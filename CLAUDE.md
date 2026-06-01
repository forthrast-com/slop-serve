# slop-serve

GitHub Pages site serving markdown files at slop.forthrast.com.

## adding posts

Drop `.md` files into `posts/`. No front matter needed. They appear on the index automatically.

## cite cleanup

Research docs exported from Claude often contain citation blobs with invisible Unicode delimiters. Strip them before committing:

```sh
python3 -c "
import re
text = open('posts/yourfile.md').read()
open('posts/yourfile.md', 'w').write(re.sub(r'cite\S+', '', text))
"
```

## DNS

`slop` CNAME → `forthrast-com.github.io`

## deployment

Merge to `main`. GitHub Pages builds automatically from the root via Jekyll.
