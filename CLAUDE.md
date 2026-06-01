# slop-serve

GitHub Pages site serving markdown files at slop.forthrast.com.

## adding posts

Drop `.md` files into `posts/`. No front matter needed. They appear on the index automatically.

## cite cleanup

Research docs exported from Claude often contain citation blobs (`citeturnNsearchN`) and invisible Unicode delimiters (U+E200). The pipeline handles this automatically via `.github/workflows/clean-posts.yml`, which runs on every push that touches `posts/`.

To clean manually before committing:

```sh
python3 scripts/clean-posts.py posts/*.md
```

The script strips cite blobs, invisible delimiters, and drops table columns that are entirely citation content (e.g. a "Sources" column).

## DNS

`slop` CNAME → `forthrast-com.github.io`

## deployment

Merge to `main`. GitHub Pages builds automatically from the root via Jekyll.

This is a rapid project — commit directly to `main` or merge feature branches straight in without ceremony. No PR review required.
