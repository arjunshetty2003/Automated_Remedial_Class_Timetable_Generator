# 🚨 SECURITY ALERT - Action Required

## ⚠️ Issue Detected

Your **Supabase service role key** was committed to Git in `.mcp.json` and may be publicly exposed if pushed to GitHub.

**Commit**: `0838b9f - Completed backend`

---

## 🔥 IMMEDIATE ACTIONS REQUIRED

### 1. Rotate Your Supabase Service Role Key (DO THIS NOW!)

1. Go to: https://supabase.com/dashboard
2. Select your project: `lxizswzgdzjzsonekqdx`
3. Navigate to: **Settings** → **API**
4. Under **Project API keys**, find **service_role key**
5. Click **Generate new key** (or similar option)
6. Copy the new key
7. Update your local `.mcp.json` with the new key
8. The old key will be invalidated

### 2. Check if Pushed to GitHub

```bash
git remote -v
```

If you see a GitHub remote and you've pushed:
- The key is **publicly exposed**
- Anyone can access your database with full admin rights
- **Rotate the key immediately** (step 1)

### 3. Git Cleanup (Already Done ✅)

- ✅ Added `.mcp.json` to `.gitignore`
- ✅ Removed `.mcp.json` from Git tracking
- ✅ Created `.mcp.json.example` template

### 4. Commit the Security Fix

```bash
git add .gitignore .mcp.json.example
git commit -m "Security: Remove sensitive keys from git tracking"
git push
```

### 5. Remove from Git History (If Already Pushed)

If you already pushed to GitHub, you need to remove the key from history:

**Option A: Using BFG Repo Cleaner (Recommended)**
```bash
# Install BFG
brew install bfg  # macOS

# Clone a fresh copy
git clone --mirror git@github.com:yourusername/yourrepo.git
cd yourrepo.git

# Remove the file from history
bfg --delete-files .mcp.json

# Clean and push
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**Option B: Using git filter-branch**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .mcp.json" \
  --prune-empty --tag-name-filter cat -- --all

git push --force --all
```

⚠️ **Warning**: Force pushing rewrites history. Coordinate with team members if this is a shared repo.

---

## 📋 Post-Incident Checklist

After rotating the key:

- [ ] New service role key generated in Supabase
- [ ] Local `.mcp.json` updated with new key
- [ ] `.mcp.json` added to `.gitignore`
- [ ] Git history cleaned (if key was pushed)
- [ ] Verified old key no longer works
- [ ] Team members notified (if shared repo)
- [ ] Monitor Supabase logs for suspicious activity

---

## 🔒 Best Practices Going Forward

### 1. Never commit these files:
- `.env`
- `.mcp.json`
- Any file with API keys, passwords, or tokens

### 2. Always use example/template files:
- `.env.example`
- `.mcp.json.example`
- Document what variables are needed

### 3. Use environment variables:
Instead of hardcoding in `.mcp.json`, reference from environment:
```json
{
  "env": {
    "SUPABASE_URL": "${SUPABASE_URL}",
    "SUPABASE_SERVICE_ROLE_KEY": "${SUPABASE_SERVICE_ROLE_KEY}"
  }
}
```

### 4. Pre-commit hooks:
Install `git-secrets` or similar tools to prevent committing secrets:
```bash
brew install git-secrets
git secrets --install
git secrets --register-aws
```

---

## 📊 What Was Exposed

**File**: `.mcp.json`
**Key Type**: Supabase Service Role Key
**Access Level**: **FULL ADMIN** - Can read, write, delete all data
**Bypasses**: Row Level Security (RLS)
**Risk**: **CRITICAL**

---

## 🆘 Need Help?

If you're unsure about any step:
1. Contact Supabase support: https://supabase.com/support
2. Check documentation: https://supabase.com/docs/guides/api/api-keys
3. Review security best practices: https://supabase.com/docs/guides/platform/going-into-prod

---

**Status**: 🔴 **CRITICAL - ACTION REQUIRED**

**Next Steps**:
1. Rotate Supabase key NOW
2. Update local `.mcp.json`
3. Commit security fixes
4. Clean git history if needed
