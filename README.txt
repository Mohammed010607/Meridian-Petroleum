Meridian Petroleum - static site
================================
index.html is the entire website. Everything is inside it:
all CSS, all JavaScript, and all 11 photographs (inline).

It needs no build step, no server-side code and no configuration.
Navigation uses URL hash routes (#/services, #/contact), which are
handled in the browser - so it works on ANY static host with zero
rewrite rules.

The only outbound request the page makes is to Google Fonts.

Deploying: upload this folder. That is the whole process.
