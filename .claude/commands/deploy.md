# Deploy — Shaingan Site

Deploy the Shaingan website to Netlify and sync to GitHub.

## Steps

1. **Git — stage and commit all changes**
   ```powershell
   cd "D:\Profiles\Documents\Claude"
   git add .
   git commit -m "deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
   git push origin master
   ```

2. **Netlify — deploy to production**
   ```powershell
   $env:PATH += ";C:\Program Files\nodejs"
   & "C:\Users\Bruno\AppData\Roaming\npm\netlify.cmd" deploy --prod --dir "D:\Profiles\Documents\Claude\shaingan-site" --site "2892fd78-048a-4c54-b7ba-23cb2eb4540d"
   ```

3. **Report** the production URL and confirm deploy is live.

If there are no changes to commit, skip the git step and go straight to Netlify deploy.
