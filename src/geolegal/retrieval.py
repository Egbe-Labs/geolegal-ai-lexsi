"""Deterministic lexical retrieval over approved source records."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping

from geolegal.run_registry import fingerprint
from geolegal.schema import Jurisdiction, SourceRecord

TOKEN_PATTERN = re.compile(r"[\w'-]+", re.UNICODE)


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(TOKEN_PATTERN.findall(text.casefold()))


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    passage_id: str
    provision: str
    url: str
    text: str
    score: float
    rank: int
    source_hash: str

    def prompt_dict(self) -> dict[str, str]:
        # Delimit source text as untrusted data. Model instructions live only in the system prompt.
        escaped = self.text.replace("<SOURCE_TEXT>", "&lt;SOURCE_TEXT&gt;").replace(
            "</SOURCE_TEXT>", "&lt;/SOURCE_TEXT&gt;"
        )
        return {
            "passage_id": self.passage_id,
            "provision": self.provision,
            "url": self.url,
            "text": f"<SOURCE_TEXT>\n{escaped}\n</SOURCE_TEXT>",
        }


class LexicalRetriever:
    def __init__(self, sources: Iterable[SourceRecord], *, top_k: int = 4) -> None:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        self.sources = tuple(sorted(sources, key=lambda item: item.source_id))
        if len({source.source_id for source in self.sources}) != len(self.sources):
            raise ValueError("Source IDs must be unique")
        self.top_k = top_k
        self.revision = fingerprint(
            {
                "algorithm": "lexical-tf-v1",
                "top_k": top_k,
                "sources": [
                    {"source_id": source.source_id, "content_hash": source.content_hash}
                    for source in self.sources
                ],
            }
        )

    def retrieve(self, query: str, jurisdiction: Jurisdiction) -> tuple[RetrievalResult, ...]:
        query_terms = set(tokenize(query))
        scored: list[tuple[float, SourceRecord]] = []
        for source in self.sources:
            if source.jurisdiction is not jurisdiction:
                continue
            counts = Counter(tokenize(f"{source.provision} {source.title} {source.text}"))
            overlap = sum(1.0 + math.log(counts[term]) for term in query_terms if counts[term])
            if overlap:
                score = overlap / math.sqrt(sum(counts.values()))
                scored.append((score, source))
        scored.sort(key=lambda pair: (-pair[0], pair[1].source_id))
        return tuple(
            RetrievalResult(
                passage_id=source.source_id,
                provision=source.provision,
                url=source.url,
                text=source.text,
                score=round(score, 8),
                rank=rank,
                source_hash=source.content_hash,
            )
            for rank, (score, source) in enumerate(scored[: self.top_k], 1)
        )


def prompt_passages(results: Iterable[RetrievalResult]) -> tuple[Mapping[str, str], ...]:
    return tuple(result.prompt_dict() for result in results)
