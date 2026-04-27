"""
Base class for README update scripts.

This abstract base class eliminates code duplication across update scripts
by providing a common pattern for:
  1. Reading the README file
  2. Fetching fresh data
  3. Updating a specific section via regex
  4. Writing changes back
"""

import os
import re
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path


class UpdateScriptBase(ABC):
    """Abstract base class for all README update scripts."""

    # Subclasses must define these patterns for their specific sections
    SECTION_HEADER_PATTERN: str  # Regex to find the section start (e.g., table header)
    SECTION_END_PATTERN: str     # Regex to find the section end (e.g., closing tag)
    TIMESTAMP_PATTERN: str       # Regex to find the timestamp line to update

    def __init__(self, readme_path: str | None = None):
        """Initialize the update script.
        
        Args:
            readme_path: Path to README.md. If None, uses current directory.
        """
        if readme_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            readme_path = os.path.join(script_dir, "README.md")
        
        self.readme_path = readme_path
        self.now = datetime.now(timezone.utc)

    @abstractmethod
    def fetch_data(self) -> str:
        """Fetch fresh data from API or compute it.
        
        Returns:
            Formatted content to insert into the README section.
        """
        pass

    @abstractmethod
    def get_section_name(self) -> str:
        """Return human-readable name for logging (e.g., 'weather', 'stocks')."""
        pass

    def read_readme(self) -> str:
        """Read the current README file."""
        with open(self.readme_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_readme(self, content: str) -> None:
        """Write updated content back to README."""
        with open(self.readme_path, "w", encoding="utf-8") as f:
            f.write(content)

    def update_section(self, readme: str, new_content: str) -> str:
        """Replace section content using defined regex patterns.
        
        Args:
            readme: Current README content
            new_content: New content to insert
            
        Returns:
            Updated README content
        """
        # Build the replacement pattern: keep header, replace body, keep end marker
        pattern = f"({self.SECTION_HEADER_PATTERN}\n)(.*?)(\n{self.SECTION_END_PATTERN})"
        replacement = r"\1" + new_content + r"\3"
        
        updated = re.sub(pattern, replacement, readme, flags=re.DOTALL)
        
        if updated == readme:
            print(f"⚠️  Warning: No changes made for {self.get_section_name()} section")
        
        return updated

    def update_timestamp(self, readme: str) -> str:
        """Update the timestamp in the section footer.
        
        Args:
            readme: Current README content
            
        Returns:
            Updated README with new timestamp
        """
        update_time = self.now.strftime("%d %b %Y, %H:%M UTC")
        updated = re.sub(
            self.TIMESTAMP_PATTERN,
            f"<b>{update_time}</b>",
            readme
        )
        return updated

    def run(self) -> None:
        """Execute the update workflow."""
        section_name = self.get_section_name()
        print(f"📚 Reading README...")
        readme = self.read_readme()

        print(f"📡 Fetching {section_name} data...")
        new_content = self.fetch_data()

        print(f"📝 Updating {section_name} section...")
        readme = self.update_section(readme, new_content)
        readme = self.update_timestamp(readme)

        print(f"💾 Writing changes...")
        self.write_readme(readme)

        print(f"✅ {section_name.capitalize()} updated at {self.now.strftime('%Y-%m-%d %H:%M UTC')}")
