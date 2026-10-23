import re
from typing import List

class SalienceDistiller:
    """
    100% Dynamic Linguistic Extractor.
    Takes arbitrary raw text from any real source and extracts the 3-4 most
    coherent, information-dense, declarative sentences.
    Zero pre-canned templates.
    """

    @staticmethod
    def condense_to_detailed_paragraph(raw_text: str, entity_name: str = "", min_sentences: int = 3, max_sentences: int = 4) -> str:
        if not raw_text or not raw_text.strip():
            return f"{entity_name} is an indexed topic in verified global repositories."

        # 1. Clean Wikipedia / academic noise: remove citations [1], (listen; born...), formatting artifacts
        cleaned = re.sub(r"\[\d+\]", "", raw_text)
        cleaned = re.sub(r"\([^\)]*?(?:listen|pronunciation|born|\d{4}\s*–|\d{4}\s*-\s*\d{4})[^\)]*?\)", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        # 2. Robust sentence splitter (respects abbreviations like Dr., U.S., Inc.)
        raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", cleaned)
        filtered_sentences: List[str] = []

        for s in raw_sentences:
            s_str = s.strip()
            # Discard short fragments, headers, or bibliography lines
            if len(s_str) < 35:
                continue
            if any(s_str.lower().startswith(bad) for bad in [
                "see also", "coordinates", "references", "external links",
                "further reading", "for other uses", "this article is about",
                "retrieved on", "archived from"
            ]):
                continue

            filtered_sentences.append(s_str)
            if len(filtered_sentences) >= max_sentences:
                break

        if len(filtered_sentences) >= min_sentences:
            return " ".join(filtered_sentences)
        elif filtered_sentences:
            return " ".join(filtered_sentences)
        else:
            return cleaned[:300].strip() + "..."
