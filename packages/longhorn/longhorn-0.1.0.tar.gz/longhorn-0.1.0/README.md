# longhorn

![longhorn](assets/longhorn.jpg)

[Photo by Miguel from Pexels](https://www.pexels.com/photo/brown-texas-longhorn-lying-on-the-ground-12578659/)

longhorn is meant for hosting a single blog associated with a specific ActivityPub actor. Example:

- My blog is available at [https://blog.mymath.rocks/](https://blog.mymath.rocks/)
- If you follow me, i.e. `@helge@mymath.rocks`. My blog posts will be delivered to your ActivityPub Inbox as a create article.
- Public replies to that Article are displayed on the blog.

This is realized by longhorn being a [bovine](https://codeberg.org/helge/bovine/) based ActivityPub Client.

## Installation

longhorn can be installed by running

```bash
pip install longhorn
python -mlonghorn.setup
```

There you will be prompted for

- The host your blog will run on, e.g. `blog.mymath.rocks`
- The title of your blog, e.g. `Helge's blog`
- The host of your ActivityPub server, e.g. `mymath.rocks`
- And be provided a did-key to add to your ActivityPub Actor following the [BIN-2](https://blog.mymath.rocks/2023-03-25/BIN2_Moo_Client_Registration_Flow).

The blog can then be run, by running

```bash
hypercorn longhorn:app
```

## Usage

Posts are written as markdown then uploaded using

```bash
python -mlonghorn.post filename.md
```

## Todos

- [x] Stopping the server is awkward due to the Event Source loop not stopping properly. Investigate how to fix this.
- [x] Alternative to last todo: Separate Event Source into own process.
- [x] Alternative: Use webhooks
- __Solution__: Move to [mechanical bull](https://codeberg.org/bovine/mechanical_bull)
- [x] Provide an RSS feed
- [ ] Enable a publish / preview endpoint
- [ ] Explain how to customize templating without hacking the package
- [ ] Support tags and other metadata
