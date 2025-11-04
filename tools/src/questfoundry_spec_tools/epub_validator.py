"""EPUB validator for QuestFoundry - CI/QA gates enforcement.

Validates EPUB exports against post-mortem policies:
- Gate 1: Cover Policy (title-bearing PNG)
- Gate 2: Start Page Invariant (first scene, not TOC)
- Gate 3: Anchor Integrity (all links resolve, inline anchors present)
- Gate 4: Kobo Compatibility (NCX, landmarks, inline anchors)
- Gate 5: Manifest Compliance (art manifest integrity)
- Gate 6: Header Hygiene (no operational markers)
"""

import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from lxml import etree
except ImportError:
    etree = None
    print("Warning: lxml not installed. Install with: uv add lxml")


@dataclass
class ValidationResult:
    """Result of a single validation gate."""
    gate_name: str
    status: str  # "pass" | "warn" | "fail"
    message: str
    details: list[str]


class EPUBValidator:
    """Validates EPUB files against QuestFoundry quality gates."""

    NAMESPACES = {
        'opf': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'xhtml': 'http://www.w3.org/1999/xhtml',
        'epub': 'http://www.idpf.org/2007/ops',
        'ncx': 'http://www.daisy.org/z3986/2005/ncx/',
    }

    def __init__(self, epub_path: Path):
        self.epub_path = epub_path
        self.results: list[ValidationResult] = []

    def validate(self) -> tuple[bool, list[ValidationResult]]:
        """Run all validation gates. Returns (success, results)."""
        if not self.epub_path.exists():
            return False, [ValidationResult(
                "File Check",
                "fail",
                f"EPUB file not found: {self.epub_path}",
                []
            )]

        if etree is None:
            return False, [ValidationResult(
                "Dependencies",
                "fail",
                "lxml library not installed. Run: uv add lxml",
                []
            )]

        try:
            with zipfile.ZipFile(self.epub_path, 'r') as epub:
                self._gate_1_cover_policy(epub)
                self._gate_2_start_page(epub)
                self._gate_3_anchor_integrity(epub)
                self._gate_4_kobo_compat(epub)
                # self._gate_5_manifest_compliance(epub)  # Requires art_manifest.json access
                self._gate_6_header_hygiene(epub)
        except Exception as e:
            self.results.append(ValidationResult(
                "EPUB Parsing",
                "fail",
                f"Error parsing EPUB: {e}",
                []
            ))
            return False, self.results

        # Determine overall success
        has_failures = any(r.status == "fail" for r in self.results)
        return not has_failures, self.results

    def _gate_1_cover_policy(self, epub: zipfile.ZipFile):
        """Gate 1: Cover Policy - title-bearing PNG required."""
        details = []

        # Read content.opf
        opf_path = self._find_opf(epub)
        if not opf_path:
            self.results.append(ValidationResult(
                "Gate 1: Cover Policy",
                "fail",
                "content.opf not found",
                []
            ))
            return

        opf_content = epub.read(opf_path)
        opf_tree = etree.fromstring(opf_content)

        # Find cover meta
        cover_id = opf_tree.xpath(
            '//opf:metadata/opf:meta[@name="cover"]/@content',
            namespaces=self.NAMESPACES
        )

        if not cover_id:
            self.results.append(ValidationResult(
                "Gate 1: Cover Policy",
                "fail",
                "No cover-image meta tag found in content.opf",
                ["Add: <meta name=\"cover\" content=\"cover-image\"/>"]
            ))
            return

        # Find cover item in manifest
        cover_item = opf_tree.xpath(
            f'//opf:manifest/opf:item[@id="{cover_id[0]}"]',
            namespaces=self.NAMESPACES
        )

        if not cover_item:
            self.results.append(ValidationResult(
                "Gate 1: Cover Policy",
                "fail",
                f"Cover item '{cover_id[0]}' not found in manifest",
                []
            ))
            return

        media_type = cover_item[0].get('media-type', '')
        href = cover_item[0].get('href', '')

        # Check if PNG
        if 'png' not in media_type.lower() and not href.lower().endswith('.png'):
            self.results.append(ValidationResult(
                "Gate 1: Cover Policy",
                "warn",
                f"Cover is not PNG format: {media_type}",
                ["Recommended: Use title-bearing PNG as primary cover"]
            ))
        else:
            details.append(f"Cover image: {href} ({media_type})")
            details.append("✓ Cover is PNG format")

        # Check for SVG backup
        svg_backup = opf_tree.xpath(
            '//opf:manifest/opf:item[contains(@media-type, "svg")]',
            namespaces=self.NAMESPACES
        )
        if svg_backup:
            details.append("✓ SVG backup cover found")

        self.results.append(ValidationResult(
            "Gate 1: Cover Policy",
            "pass",
            "Cover policy validated",
            details
        ))

    def _gate_2_start_page(self, epub: zipfile.ZipFile):
        """Gate 2: Start Page Invariant - reading order begins at first scene."""
        details = []

        opf_path = self._find_opf(epub)
        if not opf_path:
            return

        opf_content = epub.read(opf_path)
        opf_tree = etree.fromstring(opf_content)

        # Get first itemref in spine
        first_itemref = opf_tree.xpath(
            '//opf:spine/opf:itemref[1]/@idref',
            namespaces=self.NAMESPACES
        )

        if not first_itemref:
            self.results.append(ValidationResult(
                "Gate 2: Start Page",
                "fail",
                "No spine items found",
                []
            ))
            return

        # Find corresponding manifest item
        first_item = opf_tree.xpath(
            f'//opf:manifest/opf:item[@id="{first_itemref[0]}"]/@href',
            namespaces=self.NAMESPACES
        )

        if first_item:
            href = first_item[0]
            details.append(f"First spine item: {href}")

            # Check if it matches scene pattern (e.g., 001.xhtml, section-*.xhtml)
            if re.match(r'^\d{3}\.xhtml$', href) or re.match(r'^section-.*\.xhtml$', href):
                details.append("✓ Reading order starts at scene section")
                status = "pass"
                message = "Start page validated"
            else:
                details.append("⚠ First spine item may not be a scene")
                status = "warn"
                message = "First spine item should be a scene section (e.g., 001.xhtml)"
        else:
            status = "fail"
            message = f"First spine item '{first_itemref[0]}' not found in manifest"

        self.results.append(ValidationResult(
            "Gate 2: Start Page",
            status,
            message,
            details
        ))

    def _gate_3_anchor_integrity(self, epub: zipfile.ZipFile):
        """Gate 3: Anchor Integrity - all links resolve, inline anchors present."""
        details = []
        anchors_found = set()
        links_found = []
        inline_anchor_count = 0
        section_count = 0

        opf_path = self._find_opf(epub)
        if not opf_path:
            return

        # Get all XHTML files from manifest
        opf_content = epub.read(opf_path)
        opf_tree = etree.fromstring(opf_content)

        xhtml_items = opf_tree.xpath(
            '//opf:manifest/opf:item[contains(@media-type, "xhtml")]/@href',
            namespaces=self.NAMESPACES
        )

        opf_dir = Path(opf_path).parent

        for href in xhtml_items:
            file_path = str(opf_dir / href)
            if file_path not in epub.namelist():
                continue

            try:
                xhtml_content = epub.read(file_path)
                xhtml_tree = etree.fromstring(xhtml_content)

                # Find all elements with id attribute
                ids = xhtml_tree.xpath('//*/@id')
                for id_val in ids:
                    anchors_found.add(f"{href}#{id_val}")

                # Count inline anchors (a or span with id)
                inline_anchors = xhtml_tree.xpath(
                    '//xhtml:a[@id] | //xhtml:span[@id]',
                    namespaces=self.NAMESPACES
                )
                inline_anchor_count += len(inline_anchors)

                # Count sections
                sections = xhtml_tree.xpath(
                    '//xhtml:section | //xhtml:div[@class="section"]',
                    namespaces=self.NAMESPACES
                )
                section_count += len(sections)

                # Find all links
                links = xhtml_tree.xpath('//xhtml:a/@href', namespaces=self.NAMESPACES)
                for link in links:
                    if '#' in link:
                        links_found.append((href, link))
            except Exception as e:
                details.append(f"⚠ Error parsing {href}: {e}")

        # Validate links
        broken_links = []
        for source_file, link in links_found:
            if link.startswith('#'):
                # Same-file anchor
                target = f"{source_file}{link}"
            elif '#' in link:
                # Cross-file anchor
                target_file, anchor = link.split('#', 1)
                target = f"{target_file}#{anchor}"
            else:
                continue  # External link, skip

            if target not in anchors_found:
                broken_links.append(f"{source_file} → {link}")

        details.append(f"Total anchors: {len(anchors_found)}")
        details.append(f"Total links: {len(links_found)}")
        details.append(f"Inline anchors: {inline_anchor_count}")
        details.append(f"Sections: {section_count}")

        if broken_links:
            self.results.append(ValidationResult(
                "Gate 3: Anchor Integrity",
                "fail",
                f"{len(broken_links)} broken link(s) found",
                details + [f"Broken: {link}" for link in broken_links[:10]]  # First 10
            ))
        else:
            details.append("✓ All links resolve")
            if inline_anchor_count >= section_count:
                details.append("✓ Inline anchors present (Kobo compat)")
            else:
                details.append(f"⚠ Only {inline_anchor_count}/{section_count} sections have inline anchors")

            self.results.append(ValidationResult(
                "Gate 3: Anchor Integrity",
                "pass",
                "All links resolve",
                details
            ))

    def _gate_4_kobo_compat(self, epub: zipfile.ZipFile):
        """Gate 4: Kobo Compatibility - NCX, landmarks, inline anchors."""
        details = []

        opf_path = self._find_opf(epub)
        if not opf_path:
            return

        opf_content = epub.read(opf_path)
        opf_tree = etree.fromstring(opf_content)

        # Check for NCX in manifest
        ncx_items = opf_tree.xpath(
            '//opf:manifest/opf:item[@media-type="application/x-dtbncx+xml"]',
            namespaces=self.NAMESPACES
        )

        if ncx_items:
            details.append("✓ toc.ncx present in manifest")

            # Verify NCX file exists and has content
            ncx_href = ncx_items[0].get('href')
            opf_dir = Path(opf_path).parent
            ncx_path = str(opf_dir / ncx_href)

            if ncx_path in epub.namelist():
                ncx_content = epub.read(ncx_path)
                ncx_tree = etree.fromstring(ncx_content)

                nav_points = ncx_tree.xpath('//ncx:navPoint', namespaces=self.NAMESPACES)
                details.append(f"  NCX nav points: {len(nav_points)}")

                # Check playOrder is sequential
                play_orders = ncx_tree.xpath('//ncx:navPoint/@playOrder', namespaces=self.NAMESPACES)
                if play_orders:
                    play_orders_int = [int(po) for po in play_orders]
                    if play_orders_int == list(range(1, len(play_orders) + 1)):
                        details.append("  ✓ playOrder is sequential (1..N)")
                    else:
                        details.append(f"  ⚠ playOrder not sequential: {play_orders_int[:5]}...")
        else:
            details.append("✗ toc.ncx missing (Kobo devices may have navigation issues)")

        # Check for landmarks in nav.xhtml
        nav_items = opf_tree.xpath(
            '//opf:manifest/opf:item[@properties="nav"]/@href',
            namespaces=self.NAMESPACES
        )

        if nav_items:
            opf_dir = Path(opf_path).parent
            nav_path = str(opf_dir / nav_items[0])

            if nav_path in epub.namelist():
                nav_content = epub.read(nav_path)
                nav_tree = etree.fromstring(nav_content)

                landmarks = nav_tree.xpath(
                    '//xhtml:nav[@epub:type="landmarks"]',
                    namespaces=self.NAMESPACES
                )

                if landmarks:
                    details.append("✓ ARIA landmarks present in nav.xhtml")

                    # Count landmark types
                    landmark_types = nav_tree.xpath(
                        '//xhtml:nav[@epub:type="landmarks"]//xhtml:a/@epub:type',
                        namespaces=self.NAMESPACES
                    )
                    details.append(f"  Landmark types: {', '.join(landmark_types)}")
                else:
                    details.append("⚠ ARIA landmarks missing from nav.xhtml")

        # Check for EPUB2 guide
        guide = opf_tree.xpath('//opf:guide/opf:reference', namespaces=self.NAMESPACES)
        if guide:
            details.append(f"✓ EPUB2 guide present ({len(guide)} references)")
        else:
            details.append("  (Optional) EPUB2 guide not present")

        # Overall status
        has_ncx = bool(ncx_items)
        if has_ncx:
            status = "pass"
            message = "Kobo compatibility features present"
        else:
            status = "warn"
            message = "Missing NCX - may have issues on Kobo devices"

        self.results.append(ValidationResult(
            "Gate 4: Kobo Compatibility",
            status,
            message,
            details
        ))

    def _gate_6_header_hygiene(self, epub: zipfile.ZipFile):
        """Gate 6: Header Hygiene - no operational markers in section titles."""
        details = []
        violations = []

        # Pattern for operational markers
        marker_pattern = re.compile(
            r'^\s*(Hub|Unofficial|Quick|Temp|Draft|FLAG_\w+|CODEWORD)\s*:\s*',
            re.IGNORECASE
        )

        opf_path = self._find_opf(epub)
        if not opf_path:
            return

        opf_content = epub.read(opf_path)
        opf_tree = etree.fromstring(opf_content)

        xhtml_items = opf_tree.xpath(
            '//opf:manifest/opf:item[contains(@media-type, "xhtml")]/@href',
            namespaces=self.NAMESPACES
        )

        opf_dir = Path(opf_path).parent

        for href in xhtml_items:
            file_path = str(opf_dir / href)
            if file_path not in epub.namelist():
                continue

            try:
                xhtml_content = epub.read(file_path)
                xhtml_tree = etree.fromstring(xhtml_content)

                # Find all h2 headings (section titles)
                headings = xhtml_tree.xpath(
                    '//xhtml:h2 | //xhtml:h1',
                    namespaces=self.NAMESPACES
                )

                for heading in headings:
                    text = heading.text or ''
                    if marker_pattern.match(text):
                        violations.append(f"{href}: {text}")
            except Exception as e:
                details.append(f"⚠ Error parsing {href}: {e}")

        if violations:
            self.results.append(ValidationResult(
                "Gate 6: Header Hygiene",
                "fail",
                f"{len(violations)} header(s) contain operational markers",
                details + [
                    "Move markers to section metadata (kind: hub, route: unofficial, pace: quick)",
                    "Violations:"
                ] + violations[:10]  # First 10
            ))
        else:
            details.append("✓ No operational markers in headers")
            self.results.append(ValidationResult(
                "Gate 6: Header Hygiene",
                "pass",
                "Header hygiene validated",
                details
            ))

    def _find_opf(self, epub: zipfile.ZipFile) -> Optional[str]:
        """Find content.opf path in EPUB."""
        # Check META-INF/container.xml
        try:
            container_content = epub.read('META-INF/container.xml')
            container_tree = etree.fromstring(container_content)

            rootfile = container_tree.xpath(
                '//container:rootfile/@full-path',
                namespaces={'container': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            )

            if rootfile:
                return rootfile[0]
        except Exception:
            pass

        # Fallback: search for content.opf
        for name in epub.namelist():
            if name.endswith('content.opf'):
                return name

        return None


def format_results(results: list[ValidationResult]) -> str:
    """Format validation results as human-readable report."""
    lines = []
    lines.append("=" * 70)
    lines.append("EPUB Validation Report")
    lines.append("=" * 70)
    lines.append("")

    for result in results:
        icon = {"pass": "✓", "warn": "⚠", "fail": "✗"}[result.status]
        lines.append(f"{icon} {result.gate_name}: {result.message}")

        if result.details:
            for detail in result.details:
                lines.append(f"  {detail}")

        lines.append("")

    # Summary
    passed = sum(1 for r in results if r.status == "pass")
    warned = sum(1 for r in results if r.status == "warn")
    failed = sum(1 for r in results if r.status == "fail")

    lines.append("=" * 70)
    lines.append(f"Summary: {passed} passed, {warned} warnings, {failed} failed")
    lines.append("=" * 70)

    return "\n".join(lines)


def validate_epub_cli():
    """CLI entry point for EPUB validation."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: qfspec-validate-epub <path-to-epub>")
        sys.exit(1)

    epub_path = Path(sys.argv[1])
    validator = EPUBValidator(epub_path)

    success, results = validator.validate()
    print(format_results(results))

    sys.exit(0 if success else 1)
