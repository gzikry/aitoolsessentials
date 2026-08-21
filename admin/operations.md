# AIToolsEssentials Operations Guide

**Last Updated:** 2026-08-21  
**Status:** ✅ Fully Operational

## Quick Links
- **Site:** https://aitoolessentials.com
- **Admin Dashboard:** `/admin/operations.html`
- **Operations Guide:** `/admin/operations.md`

---

## 🚀 Site Overview

**39 AI tools** reviewed  
**19 category buyer guides**  
**145 public pages** + 4 admin pages  
**Sitemap:** 145 URLs  

### Revenue Infrastructure
- ✅ 16 high-priority affiliate programs configured
- ✅ 5 sponsorship placement types defined
- ✅ Scorecard download (lead magnet)
- ✅ AI Stack Audit consulting ($497)
- ✅ Newsletter CTA on all pages

### Viral Growth Features
- ✅ `/leaderboard.html` — Weekly rankings with FOMO
- ✅ `/submit-tool.html` — One-click submission
- ✅ Social sharing buttons on all pages
- ✅ OG images for Twitter/LinkedIn

---

## 📅 Daily Automation

**Cron Job:** "AIToolsEssentials Daily Maintenance"  
**Schedule:** Daily at 8 AM UTC (1 AM local)

### What It Does
1. **Regenerates all tool review pages** from `data/tools.json`
2. **Updates category buyer guides**
3. **Adds social sharing buttons** to new pages
4. **Regenerates sitemap.xml**
5. **Writes daily content brief** to `content_briefs/YYYY-MM-DD-daily-content-brief.md`

### Manual Run
```bash
cd /Users/georgezikry/aitoolessentials/site
python3 scripts/daily_content_update.py
python3 scripts/validate_site.py
```

---

## 📊 Revenue System

### Affiliate Programs
**File:** `data/affiliate_programs.json`  
**High Priority:** 16 tools

**Apply for:**
1. Gamma (AI presentations)
2. Jasper (AI writing)
3. Copy.ai (AI copywriting)
4. Midjourney (AI art)
5. Grammarly (AI writing)
6. etc.

### Sponsorship Placements
**File:** `data/sponsor_inventory.json`

**Placement Types:**
1. **Hero Banner** — Top of page, 728x90px
2. **Content Inline** — Between tool reviews
3. **Sidebar** — Right sidebar, 300x250px
4. **Category Featured** — Category page hero
5. **Newsletter Header** — Email newsletter

### Scorecard Download
**File:** `/downloads/ai-tool-evaluation-scorecard.html`  
**Purpose:** Free lead magnet for email capture

---

## 🎯 Viral Growth Strategy

### Leaderboard Mechanics
- **Weekly reset** (Mondays)
- **Upvotes** from community
- **Click tracking** for performance
- **Premium tiers** for guaranteed rankings

### Submit Tool Form
- **One-click submission** (< 30 seconds)
- **Free listing** on leaderboard
- **Premium upgrades** for better placement

### Social Sharing
- **Twitter, Facebook, LinkedIn** buttons on all pages
- **Pre-formatted tweets** for sharing
- **OG images** for social media

---

## 📁 File Structure

```
aitoolessentials/site/
├── data/
│   ├── tools.json                    # Tool inventory (39 tools)
│   ├── affiliate_programs.json       # Affiliate network details
│   ├── revenue_targets.json          # Approval tracking
│   ├── sponsors.json                 # Sponsor placements
│   ├── sponsor_inventory.json        # Draft pricing
│   ├── newsletter.json               # Newsletter config
│   └── social_sharing.json           # Social templates
├── scripts/
│   ├── daily_content_update.py       # Main automation
│   ├── validate_site.py              # Quality gates
│   ├── add_social_sharing.py         # Social buttons
│   └── generate_ai_stack_audit.py    # Consulting reports
├── tools/                            # 39 tool review pages
│   ├── chatgpt/index.html
│   ├── claude/index.html
│   └── ...
├── categories/                       # 19 category guides
├── comparisons/                      # Head-to-head comparisons
├── articles/                         # Buyer guides
├── downloads/                        # Scorecard download
├── services/                         # AI Stack Audit
├── admin/                            # Management hub
├── content_briefs/                   # Daily briefs
├── assets/
│   └── og-ai-tools.jpg              # OG image (1200x630)
├── index.html
├── leaderboard.html
├── submit-tool.html
└── sitemap.xml
```

---

## 🛠️ Maintenance Checklist

### Daily (Automated)
- [ ] Review daily content brief
- [ ] Check for validation errors
- [ ] Monitor affiliate application status

### Weekly
- [ ] Update tool reviews in `data/tools.json`
- [ ] Refresh leaderboard rankings
- [ ] Check sponsorship leads

### Monthly
- [ ] Update revenue targets
- [ ] Review affiliate performance
- [ ] Generate new content briefs
- [ ] Audit site performance (Google Analytics)

---

## 📈 Key Metrics to Track

### Traffic
- **Pageviews** per tool page
- **Social shares** from each page
- **Time on page** for reviews
- **Click-through** to tool websites

### Revenue
- **Affiliate conversions** per tool
- **Sponsorship inquiries**
- **Scorecard downloads**
- **Audit consultations**

### Engagement
- **Leaderboard upvotes**
- **Social shares**
- **Newsletter signups**
- **Tool submissions**

---

## 🔐 Security Notes

- **No API keys** stored in code
- **No credentials** in commit history
- **All affiliate links** have `rel="sponsored noopener nofollow"`
- **Social sharing links** have `rel="nofollow"`
- **Privacy disclosure** on all content pages

---

## 📞 Support & Resources

### Documentation
- **Hermes Agent:** https://hermes-agent.nousresearch.com/docs
- **AIToolsEssentials Skill:** `skill_view(name='hermes-agent')`

### Skills to Load
- `hermes-agent` — Configuration and setup
- `popular-web-designs` — Design system guidance
- `plan` — Strategic planning

### Contact
For questions about the site infrastructure or revenue system, refer to:
- `/admin/operations.html` — Full operations dashboard
- `/legal/affiliate-disclosure.html` — Affiliate policies
- `/downloads/ai-tool-evaluation-scorecard.html` — Lead magnet

---

## 🎉 Launch Checklist

### Pre-Launch (✅ Complete)
- [x] All tool review pages generated
- [x] Category buyer guides created
- [x] Revenue config files in place
- [x] Viral pages (leaderboard, submit) built
- [x] Social sharing added
- [x] OG images created
- [x] Daily automation scheduled
- [x] Validation passing

### Post-Launch
- [ ] Apply for affiliate programs
- [ ] Pitch sponsorship deals
- [ ] Recruit 100 power users
- [ ] Launch newsletter (at 1K visitors)
- [ ] Monitor and optimize

---

**Status:** Ready for viral growth phase 🚀
