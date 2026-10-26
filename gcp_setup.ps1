# Lets GitHub Actions deploy WITHOUT a service account key (your organization blocks key creation).
# Run once from the VS Code terminal, after gcp_setup.ps1 steps 1-5 (already done).

$ProjectId     = "gcp-learn-506415"
$ProjectNumber = "441377835999"
$GitHubRepo    = "ILIASB1212/accountant_ai_agent_v3"
$DeployerEmail = "github-deployer@$ProjectId.iam.gserviceaccount.com"

gcloud config set project $ProjectId

Write-Host "== 1. identity pool for GitHub"
gcloud iam workload-identity-pools create github-pool --location=global --display-name="GitHub pool"

Write-Host "== 2. provider: only workflows of YOUR repository are accepted"
$mapping   = "google.subject=assertion.sub,attribute.repository=assertion.repository"
$condition = "assertion.repository=='$GitHubRepo'"
gcloud iam workload-identity-pools providers create-oidc github-provider `
    --location=global --workload-identity-pool=github-pool `
    --display-name="GitHub provider" `
    --issuer-uri="https://token.actions.githubusercontent.com" `
    --attribute-mapping=$mapping `
    --attribute-condition=$condition

Write-Host "== 3. that repository may act as the deployer account"
$member = "principalSet://iam.googleapis.com/projects/$ProjectNumber/locations/global/workloadIdentityPools/github-pool/attribute.repository/$GitHubRepo"
gcloud iam service-accounts add-iam-policy-binding $DeployerEmail `
    --role=roles/iam.workloadIdentityUser --member=$member | Out-Null

Write-Host "Done. Now replace deploy.yml and push."