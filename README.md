# Solar v.2

A high-performance Hugo theme for content publication built on the original [Solar v.2 theme](https://github.com/lowtechmag/solar) by Low-tech Magazine.


**Requires Hugo 0.145 or newer**

---

## 🚀 Getting Started

### Installation & Development

```bash
# Clone the repository
git clone <repository-url>
cd solar_v2

# Start development server
hugo server

# Open browser to http://localhost:1313
```

The development server watches for changes and auto-rebuilds the site.

---

## 📝 Creating Articles with YAML

All articles are created using a **YAML-based article creation system**. Instead of manually creating Hugo page bundles.

### Quick Start - Create Your First Article

**Step 1:** Create a YAML file

```bash
cp article.example.yaml my-first-article.yaml
```

**Step 2:** Edit the file with your content

```yaml
metadata:
  title: "My Article Title"           # Display name
  slug: "my-article-title"            # URL slug (kebab-case, no spaces)
  date: "2025-02-24"                  # Publication date (YYYY-MM-DD)
  summary: "Short article summary"    # Shown in article listings
  language: "en"                      # Language code
  authors:
    - "Your Name"
  categories:
    - "On Going Projects"             # Choose one category
  tags:
    - "optional"
    - "tags"

content: |
  ## Your Article Heading

  Start writing your article here in Markdown format.

  {{% figure src="image1.png" %}}
  Image caption goes here
  {{% /figure %}}

  ## Another Section

  More article content...

images:
  - filename: "image1.png"
  - filename: "image2.jpg"
  - filename: "image3.jpeg"
```

**Step 3:** Prepare your images

```bash
mkdir my-article-images/
# Copy all your images into this folder
cp ~/Downloads/*.png ~/Downloads/*.jpg my-article-images/
```

**Step 4:** Generate the article

```bash
./utils/dev.sh my-first-article.yaml --source-dir my-article-images/
```

This command:
- Parses your YAML file
- Creates the proper Hugo page bundle structure
- Dithers all images (for low-bandwidth readers)
- Reloads Hugo in your browser
- Your article is now live at `http://localhost:1313`

### YAML File Structure

```yaml
metadata:
  title: String (required)
  slug: String (required, kebab-case)
  date: YYYY-MM-DD (required)
  summary: String (required, shown in listings)
  language: "en" (required)
  authors: List (required)
    - "Author Name"
    - "Another Author"
  categories: List (required, choose one)
  tags: List (optional)
    - "tag1"
    - "tag2"
  featured_image: String (optional, filename from images/)
  draft: Boolean (optional, set to true to hide)

content: |
  # Markdown content here
  Use {{% figure src="image.png" %}}Caption{{% /figure %}} for images
  
images:
  - filename: "image1.png"
  - filename: "image2.jpg"
```

### Article Categories

Choose **exactly one** category for each article:

- **On Going Projects** - Active, ongoing work in progress
- **Project Outputs** - Completed project results and deliverables
- **Other** - Miscellaneous content

### Image Usage in Articles

```markdown
{{% figure src="my-image.png" %}}
This caption describes what the image shows
{{% /figure %}}
```

Features:
- **Automatic dithering** - Creates low-bandwidth versions for readers
- **Toggle button** - Readers can switch between dithered/original versions
- **Auto-compression** - Original images optimized to WebP format

---

## 📁 Project Structure

```
solar_v2/
├── content/                    # Article page bundles
│   ├── article-template-how-to/
│   │   ├── index.en.md
│   │   ├── images/
│   │   │   ├── image.png
│   │   │   └── dithers/
│   │   │       └── image_dithered.png
│   │   └── comments.en.md
│   └── solar-powered-website-design/
│       └── ...
│
├── layouts/                    # Hugo templates
│   ├── _default/
│   │   ├── single.html        # Article page template
│   │   ├── list.html          # Article listings
│   │   └── baseof.html        # Base template
│   └── partials/
│       ├── header.html
│       ├── footer.html
│       ├── nav.html
│       └── figure.html        # Image shortcode template
│
├── assets/css/                 # SCSS stylesheets
│   └── style.scss
│
├── static/                     # Static files
│   ├── js/
│   │   └── script.js          # Image toggle, menu toggle
│   └── icons/
│
├── utils/                      # Utility scripts
│   ├── dev.sh                 # Article generation + Hugo dev server
│   ├── create_article.py      # YAML parser
│   ├── dither_images.py       # Image dithering
│   ├── calculate_size.py      # Page size calculator
│   ├── build_site.sh          # Production build script
│   └── clean_output.py        # Output cleanup
│
├── hugo.toml                   # Hugo configuration
├── article.example.yaml        # Example article template
├── README.md                   # This file
└── LICENSE                     # AGPL 3.0
```

---

## 🛠️ Utility Scripts

All scripts are in the `utils/` directory.

### Article Generation (`utils/dev.sh`)

Converts YAML articles to Hugo format and starts dev server:

```bash
./utils/dev.sh article.yaml --source-dir ./images/
```

Options:
- `--source-dir` - Directory containing article images
- Automatically dithers images
- Launches Hugo server on port 1313

### Image Dithering (`utils/dither_images.py`)

Creates low-bandwidth versions of images using dithering algorithm.

**Install dependencies:**
```bash
pip install Pillow git+https://www.github.com/hbldh/hitherdither
```

**Usage:**
```bash
# Dither all images in content folder
python3 utils/dither_images.py --directory content/

# Dither with category-based color effects
python3 utils/dither_images.py --directory content/ --colorize

# Verbose output to see progress
python3 utils/dither_images.py --directory content/ --verbose

# Remove all dithered versions
python3 utils/dither_images.py --remove --directory content/
```

Dithered images are placed in `images/dithers/` subfolder.

---

## 📄 License & Credits

**License:** AGPL 3.0 - See LICENSE file for details

### Original Theme Creators

This project is built on the Solar v.2 theme, originally created by:

- **Marie Otsuka** (https://motsuka.com/)
- **Roel Roscam Abbing** (https://test.roelof.info)
- **Marie Verdeil** (https://verdeil.net/)

With contributions from:
- **Erhard Maria Klein** (http://www.weitblick.de/)

### Original Project

- [Solar v.2 GitHub Repository](https://github.com/lowtechmag/solar)
- [Low-tech Magazine](https://solar.lowtechmagazine.com)

---

## 📖 Learn More

### Hugo Documentation

- [Hugo Getting Started](https://gohugo.io/getting-started/)
- [Page Bundles](https://gohugo.io/content-management/page-bundles/)
- [Markdown Guide](https://gohugo.io/content-management/formats/)

### Next Steps

1. **Create your first article** using `article.example.yaml`
2. **Add images** to your article folder
3. **Run `./utils/dev.sh`** to generate and preview
4. **Test on mobile** to check responsiveness
5. **Deploy** using `hugo && scp -r public/* server:/path`

---

**Happy writing! 🌻**
