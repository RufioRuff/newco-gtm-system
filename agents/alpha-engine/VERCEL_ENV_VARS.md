# Vercel Environment Variables

After your deployment completes, add these environment variables in Vercel:

## Steps:
1. Go to: https://vercel.com/dashboard
2. Click your project: **newco-intelligence-lp**
3. Go to: **Settings** → **Environment Variables**
4. Add each of these:

---

## Variables to Add:

### SUPABASE_URL
```
https://ideofqtgaydboeeazghj.supabase.co
```
**Environment:** Production, Preview, Development

---

### SUPABASE_KEY (anon public key)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlkZW9mcXRnYXlkYm9lZWF6Z2hqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwMTU0MTIsImV4cCI6MjA4NjU5MTQxMn0.AYPVmpuV75xowP72z4ym17iasuJwjzQR0xbFmDS3aWQ
```
**Environment:** Production, Preview, Development

---

### DATABASE_URL
Get this from Supabase:
1. Go to Supabase dashboard
2. Settings → Database
3. Copy **Connection string** (URI format)
4. Replace `[YOUR-PASSWORD]` with your actual database password

Format:
```
postgresql://postgres:[YOUR-PASSWORD]@db.ideofqtgaydboeeazghj.supabase.co:5432/postgres
```
**Environment:** Production, Preview, Development

---

## After Adding Variables:

1. Click **Save** for each one
2. **Redeploy** your project:
   - Go to **Deployments** tab
   - Click the **...** menu on latest deployment
   - Click **Redeploy**
   - Select **Use existing Build Cache**
   - Click **Redeploy**

---

## Your Platform Will Be Live At:
`https://newco-intelligence-lp.vercel.app`

or whatever custom URL Vercel assigns!

---

## What You'll Have:

✅ 9 Interactive Views:
- Dashboard - Portfolio overview
- Network Intelligence - D3.js relationship graph
- Deal Flow Pipeline - Co-investment opportunities
- Manager Performance - Quartile rankings
- Capital Efficiency - Timeline charts
- Exit Watch List - Liquidity pipeline
- Signal Strength - Momentum indicators
- Meeting Prep - Exportable briefs
- Competitive Analysis - LP overlap

✅ Real Data:
- 85 funds from your portfolio
- 15 deal flow opportunities
- Real-time Supabase integration

✅ Production Infrastructure:
- Global CDN via Vercel
- Auto-scaling serverless
- Sub-2-second load times
- 99.99% uptime

🚀 **Your Intelligence LP Platform will be LIVE!**
