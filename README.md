# ldraw_parts

This is a clone of the LDraw parts library created and maintained by [LDraw.org](https://www.ldraw.org/).
This repository, and the part files in it, are optimized for use with [Web Lic](https://github.com/remig/web_lic).

The biggest difference between this part library and the official one is the flat file hierarchy: everything in the 'p' folder now lives in 'parts'.
This is obviously worse for manually working with the part folders, but this greatly simplifies finding a part - now there's just one folder to look in.

Without this flat hierarchy, a web app like Lic either has to issue multiple front end HTTP requests, one in 'parts' then, failing that, one in 'p', or it needs some back end part name mapping to correctly resolve the desired folder.
Neither solution is ideal; the first is very slow while the second is very complicated, given that Lic has no back end anything.
