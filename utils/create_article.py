#!/usr/bin/env python3
"""
Create article structure from YAML definition.

Usage:
    python3 scripts/create_article.py article.yaml [--source-dir ./images]
    python3 scripts/create_article.py article.yaml --dry-run
"""

import os
import sys
import yaml
import argparse
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


def load_article_yaml(yaml_file):
    """Load and validate article YAML file."""
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"Article file not found: {yaml_file}")
    
    with open(yaml_file, 'r') as f:
        article = yaml.safe_load(f)
    
    if not article:
        raise ValueError("YAML file is empty")
    
    return article


def validate_metadata(metadata):
    """Validate required metadata fields."""
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be a dictionary")
    
    required = ['title', 'slug', 'date', 'summary', 'language', 'authors', 'categories']
    
    for field in required:
        if field not in metadata:
            raise ValueError(f"Missing required field: metadata.{field}")
    
    # Validate slug format (no special chars, only lowercase + hyphens)
    slug = metadata['slug']
    if not all(c.isalnum() or c in '-_' for c in slug):
        raise ValueError(f"Invalid slug format: '{slug}' (only alphanumeric, hyphens, underscores allowed)")
    
    # Validate date format
    date_val = metadata['date']
    if isinstance(date_val, str):
        try:
            datetime.strptime(date_val, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format: '{date_val}' (use YYYY-MM-DD)")
    
    # Validate authors is list
    if not isinstance(metadata['authors'], list):
        raise ValueError("authors must be a list")
    
    # Validate categories is list
    if not isinstance(metadata['categories'], list):
        raise ValueError("categories must be a list")


def create_folder_structure(slug, dry_run=False):
    """Create article folder and subfolders."""
    base_path = f"content/{slug}"
    images_path = f"{base_path}/images"
    
    if dry_run:
        print(f"  [DRY RUN] Would create: {base_path}")
        print(f"  [DRY RUN] Would create: {images_path}")
    else:
        os.makedirs(images_path, exist_ok=True)
        print(f"  ✓ Created folder structure: {base_path}")
    
    return base_path


def generate_frontmatter(metadata):
    """Generate Hugo front matter from metadata."""
    # Date string
    date_val = metadata['date']
    if not isinstance(date_val, str):
        date_val = date_val.strftime('%Y-%m-%d')
    
    # Format authors array for YAML
    authors = metadata['authors']
    if len(authors) == 1:
        authors_str = f'["{authors[0]}"]'
    else:
        authors_str = '["' + '", "'.join(authors) + '"]'
    
    # Format categories array for YAML
    categories = metadata['categories']
    if len(categories) == 1:
        categories_str = f'["{categories[0]}"]'
    else:
        categories_str = '["' + '", "'.join(categories) + '"]'
    
    featured_image = metadata.get('featured_image', 'featured.png')
    
    frontmatter = f"""---
title: "{metadata['title']}"
date: "{date_val}"
summary: "{metadata['summary']}"
lang: "{metadata['language']}"
authors: {authors_str}
categories: {categories_str}
tags: {metadata.get('tags', '[]')}
type: "posts"
draft: false
featured_image: "{featured_image}"
---
"""
    return frontmatter


def create_markdown_file(base_path, metadata, content, dry_run=False):
    """Create index.en.md with front matter and content."""
    language = metadata['language']
    filepath = f"{base_path}/index.{language}.md"
    
    frontmatter = generate_frontmatter(metadata)
    full_content = frontmatter + "\n" + content.strip() + "\n"
    
    if dry_run:
        print(f"  [DRY RUN] Would create: {filepath}")
        print(f"  [DRY RUN] Front matter preview (first 300 chars):")
        print("  " + frontmatter[:300].replace('\n', '\n  '))
    else:
        with open(filepath, 'w') as f:
            f.write(full_content)
        print(f"  ✓ Generated: {filepath} ({len(full_content)} bytes)")
    
    return filepath


def create_comments_template(base_path, language, dry_run=False):
    """Create empty comments file."""
    filepath = f"{base_path}/comments.{language}.md"
    
    template = """<!-- Comments from readers will appear here -->
<!-- This is a placeholder for reader comments once the system is enabled -->
"""
    
    if dry_run:
        print(f"  [DRY RUN] Would create: {filepath}")
    else:
        with open(filepath, 'w') as f:
            f.write(template)
        print(f"  ✓ Generated: {filepath}")
    
    return filepath


def copy_images(base_path, images_list, source_dir='.', dry_run=False):
    """Copy images from source directory."""
    images_path = f"{base_path}/images"
    
    if not images_list:
        print("  ℹ No images to copy")
        return []
    
    copied_images = []
    for image_info in images_list:
        if isinstance(image_info, str):
            filename = image_info
        elif isinstance(image_info, dict):
            filename = image_info.get('filename')
        else:
            continue
        
        source = os.path.join(source_dir, filename)
        dest = os.path.join(images_path, filename)
        
        if not os.path.exists(source) and not dry_run:
            print(f"  ⚠ Warning: Image not found: {source}")
            continue
        
        if dry_run:
            print(f"  [DRY RUN] Would copy: {filename} → images/")
        else:
            shutil.copy2(source, dest)
            print(f"  ✓ Copied: {filename}")
        
        copied_images.append(filename)
    
    return copied_images


def run_dithering(base_path, dry_run=False):
    """Run dithering on article images."""
    if dry_run:
        print(f"  [DRY RUN] Would dither images in: {base_path}")
        return
    
    try:
        result = subprocess.run(
            ['python3', 'utils/dither_images.py', '-d', base_path, '--colorize'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # Count dithered images from output
            dithered_count = result.stderr.count('🖼 converted')
            if dithered_count > 0:
                print(f"  ✓ Dithered {dithered_count} image(s)")
            else:
                print(f"  ✓ Dithering completed")
        else:
            print(f"  ⚠ Dithering warning: {result.stderr[:200]}")
    
    except subprocess.TimeoutExpired:
        print(f"  ⚠ Dithering timed out")
    except Exception as e:
        print(f"  ⚠ Could not run dithering: {e}")


def validate_structure(base_path):
    """Validate article structure after creation."""
    errors = []
    
    # Check for index file
    index_files = [f for f in os.listdir(base_path) if f.startswith('index.') and f.endswith('.md')]
    if not index_files:
        errors.append("No index.*.md file found")
    
    # Check for comments file
    comment_files = [f for f in os.listdir(base_path) if f.startswith('comments.') and f.endswith('.md')]
    if not comment_files:
        errors.append("No comments.*.md file found")
    
    # Check for images folder
    if not os.path.isdir(os.path.join(base_path, 'images')):
        errors.append("No images/ folder found")
    
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Create article structure from YAML definition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/create_article.py article.yaml
  python3 scripts/create_article.py article.yaml --source-dir ./images
  python3 scripts/create_article.py article.yaml --dry-run
        """
    )
    parser.add_argument('yaml_file', help='Path to article.yaml file')
    parser.add_argument('--source-dir', default='.', help='Directory containing images (default: current dir)')
    parser.add_argument('--no-dither', action='store_true', help='Skip image dithering')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    try:
        # Load and validate
        print(f"📖 Loading article definition: {args.yaml_file}")
        article = load_article_yaml(args.yaml_file)
        
        metadata = article.get('metadata', {})
        content = article.get('content', '')
        images = article.get('images', [])
        
        if not metadata:
            raise ValueError("article.yaml must have a 'metadata' section")
        if not content:
            raise ValueError("article.yaml must have a 'content' section")
        
        validate_metadata(metadata)
        print(f"✓ Metadata validated")
        
        if args.dry_run:
            print(f"\n🔍 DRY RUN MODE - No changes will be made\n")
        
        # Create structure
        slug = metadata['slug']
        base_path = create_folder_structure(slug, dry_run=args.dry_run)
        
        # Generate files
        create_markdown_file(base_path, metadata, content, dry_run=args.dry_run)
        create_comments_template(base_path, metadata['language'], dry_run=args.dry_run)
        
        # Handle images
        if images:
            copy_images(base_path, images, args.source_dir, dry_run=args.dry_run)
            if not args.no_dither:
                run_dithering(base_path, dry_run=args.dry_run)
        
        # Validate structure (only if not dry-run)
        if not args.dry_run:
            errors = validate_structure(base_path)
            if errors:
                print(f"\n⚠ Validation warnings:")
                for error in errors:
                    print(f"  - {error}")
        
        # Success message
        if args.dry_run:
            print(f"\n✅ Dry run successful - would create article in {base_path}")
        else:
            print(f"\n✅ Article created successfully!")
            print(f"📁 Location: {base_path}")
            print(f"\n🚀 Next steps:")
            print(f"   1. Review: {base_path}/index.{metadata['language']}.md")
            print(f"   2. Build: hugo")
            print(f"   3. Serve: hugo server")
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
