# AIToolsEssentials - Deployment & Maintenance Guide

## Quick Start

### Option 1: GitHub Pages (Recommended)

1. **Create GitHub Repository**
   - Go to https://github.com/new
   - Name: `aitoolsessentials`
   - Visibility: Public (for SEO benefits)
   - Don't initialize with README (we'll add ours)

2. **Push Your Code**
   ```bash
   cd /Users/georgezikry/aitoolessentials/site
   git remote add origin https://github.com/YOUR_USERNAME/aitoolsessentials.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings
   - Navigate to "Pages" section
   - Select branch: `main`
   - Folder: `/ (root)`
   - Click "Save"

4. **Your site will be live at:**
   `https://YOUR_USERNAME.github.io/aitoolsessentials`

### Option 2: Vercel (Fastest Deployment)

```bash
npm i -g vercel
cd /Users/georgezikry/aitoolessentials/site
vercel
```

Follow the prompts to connect your GitHub repo. Auto-deploys on every push!

### Option 3: Netlify

1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub account
4. Select `aitoolsessentials` repository
5. Deploy!

---

## Daily Maintenance

### Update Content

```bash
cd /Users/georgezikry/aitoolessentials/site

# Regenerate all tool reviews and category pages
python scripts/daily_content_update.py

# Add social sharing buttons to new pages
python scripts/add_social_sharing.py

# Validate site quality
python scripts/validate_site.py

# Regenerate sitemap
python scripts/regenerate_sitemap.py
```

### Update Specific Tools

```bash
# Edit a tool's data in content_briefs/
# Then regenerate:
python scripts/regenerate_single_tool.py <tool_name>
```

### Monitor Logs

```bash
# Check daily briefs
cat content_briefs/2026-08-21-daily-brief.txt
```

---

## GitHub Actions (Optional: Auto-Deploy)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Revenue Management

### Track Affiliate Approvals

```bash
# Check approval status
cat data/affiliate_programs.json

# Update status
cat > data/affiliate_programs.json << 'EOF'
{
  "tools": [
    {"name": "tool1", "network": "Programmatic", "status": "approved"},
    ...
  ]
}
EOF
```

### Update Sponsor Placements

Edit `data/sponsors.json` with new sponsor opportunities

---

## Troubleshooting

### Site Not Loading

1. Check FTP/GitHub Pages status
2. Verify robots.txt is correct
3. Check for 404 errors in browser console

### Content Not Updating

1. Ensure Python scripts have execute permissions
2. Check for missing dependencies: `pip install jinja2 requests`
3. Verify content_briefs directory exists

### FTP Upload Issues

The FTP account may have read-only permissions. Use:
- GitHub Pages (recommended)
- cPanel File Manager
- SFTP client (FileZilla)

---

## Next Steps

1. ✅ **Deploy to GitHub Pages** (15 minutes)
2. ✅ **Verify all pages load** (check homepage, tools, categories)
3. ✅ **Submit sitemap** to Google Search Console
4. ✅ **Submit sitemap** to Bing Webmaster Tools
5. ✅ **Apply for affiliate programs** (start with high-priority tools)
6. ✅ **Share on social media** to drive initial traffic
7. ✅ **Set up Google Analytics** (optional, or use local tracking)

---

## Support

For issues or questions:
- Check `scripts/README.md` for script documentation
- Review `admin/operations.html` for management tools
- See `legal/editorial-methodology.html` for site policies

**Built for the AI community - stay ethical, stay helpful!** 🚀
