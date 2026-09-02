from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/release-please.yml"


def source() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_release_please_prefers_app_token_but_falls_back_on_forks():
    workflow = source()
    assert "Detect release GitHub App credentials" in workflow
    assert 'RELEASE_APP_ID: ${{ secrets.RELEASE_APP_ID }}' in workflow
    assert 'RELEASE_APP_PRIVATE_KEY: ${{ secrets.RELEASE_APP_PRIVATE_KEY }}' in workflow
    assert "if: steps.release-auth.outputs.use_app == 'true'" in workflow
    assert "falling back to GITHUB_TOKEN" in workflow
    fallback = "${{ steps.app-token.outputs.token || github.token }}"
    assert workflow.count(fallback) == 4


def test_release_please_keeps_write_permissions_for_builtin_token_fallback():
    workflow = source()
    assert "permissions:\n  contents: write\n  pull-requests: write\n" in workflow
