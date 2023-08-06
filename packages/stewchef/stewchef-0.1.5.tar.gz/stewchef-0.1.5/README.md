# **StewChef: Cook up some RegiSoup**

`StewChef` is a MediaWiki API wrapper for [`RegiSoup`](https://pypi.org/project/regisoup/). It was developed since I came to the realization that I cannot edit the contents of a Wiki's `.xml` dump manually as each `<text>` block is also given a size in bytes and a `sha1` hash. The next easiest approach was to edit pages while they are already on the Wiki and that is possible through MediaWiki's API.  

## **Usage:**
First, to use `StewChef`, we must create a `config.toml` file where the API endpoint URL and bot credentials are specified. In your projects working directory create a `.toml` file anyway you like or with the command line as such:
```
nano config.toml
```
and enter the following contents:
```
[server]
url = "[SERVER_IP]/api.php"

[bot]
user = "[BOT_USERNAME]"
password = "[BOT_PASSWORD]"
```
where `[SERVER_IP]` is the IP address **or** URL of the MediaWiki's API endpoint and `[BOT_USERNAME]` and `[BOT_PASSWORD]` are bot credentials that are generated on the Wiki itself (See subsection Generating bot credentials for more information.). If the login credentials are invalid then you will get a warning that you did not log in properly. While it is actually true that you could technically list and query pages without being logged in, `StewChef` currently does not support that. It decides if you are logged in based on what `CSRF` token is returned. If it is the general `+\\` token, then login actually failed and no edits will be committed to the Wiki, even though no error is raised if you try and edit the Wiki using this token. Just nothing happens.

### **Subcommands:**
After configuration we can move on to calling `StewChef`'s subcommands.
Currently the module consists of only 2 subcommands. One which is actually the mass modification tool and the other is meant more as a debug helper tool.

#### **`stewchef single`**
This command is meant more as the debug helper tool as it only gets the contents of one page. It is meant to make direct debugging of RegiSoup easier by retrieving pages from the Wiki. Usage is simple but you need to already know what you're looking for meaning the title. There is currently no way to search by title and then select. I might add that as a feature later on if I'll require it. Anyhow, it is generally meant that you run `stewchef feast` first which will print out the titles of the pages on the Wiki.
Basic usage is meant as follows:
```
stewchef single [page_title]
```
This will just output the page contents to stdout. To explicitly save as a file you must supply the command with the ``--save` flag. By default the file save path is the page's title with the spaces removed but you can specify your own save path as such:
```
stewchef single --save [page_title] config.toml [save_path]
```
Additionally the page can be saved as HTML by adding the flag `--as-html` and be made more verbose by adding `--verbose`. You can always get a reminder for this information by running:
```
stewchef single --help
```

#### **`stewchef feast`**
This command is what `StewChef` was actually made to do: Mass modify pages via RegiSoup. Usage is pretty straight forward and I implore you to run:
```
stewchef feast --help
```
for more information and a reminder during work with the tool. Anyhow supplying just the config file (defaulted to `config.toml` as created above) already allows the command to run:
```
stewchef feast
```
It will actually retrieve pages from the Wiki and parse them with RegiSoup but then do nothing with that information for which you will get a passive aggressive success message. The use case for this bare command is to get page titles I suppose but you can get that regardless, even if you supply additional tags. Actually the best way of getting just page titles is to call:
```
stewchef feast --dry-run
```
which will only retrieve page titles from the Wiki but not send the contents to RegiSoup.
Anyhow, to get `StewChef` to do something with the data you must supply it with a flag. Probably the first thing you'd like to do is to check what changes `StewChef` would like to make. This can be done with
```
stewchef feast --diff
```
`StewChef` will create a directory `./diff/` and for each page title it finds on the Wiki, save a `.diff` file named after the individual page's title. These files show a delta between the pre-RegiSoup and post-RegiSoup processing page contents. Have a look at at least some of these pages since reverting changes mass made to a Wiki is not as simple (or at least I haven't yet found an easy way). If you're satisfied with all the changes, then that is it and the next use case is:
```
stewchef feast --commit
```
This will currently actually reprocess all the pages due to the way the code is written and then commit the changes to the Wiki. I might in the future add a feature where changes can be committed directly from the `.diff` files themselves which would greatly save on time, especially for larger Wiki's.  

If you'd like to see what RegiSoup spits out during processing then supply the command with the `--regisoup-out` flag and additionally `feast` can be made more verbose with `--verbose`.

### **Getting bot credentials**
Bot credentials are generated on a page called **Bot Passwords** that you can find on your **Special: Pages** page on the Wiki. You must be logged in as an administrator to be able to generate credentials for a bot. Grant the bot the required permissions to query and edit the Wiki (or in my case I just granted it all permissions by ticking all the boxes available) and give MediaWiki a name for the bot. It will generate for you a `[BOT_USERNAME]` based on your username as well as a random `[BOT_PASSWORD]`. Enter these into your `config.toml` file at the configuration phase of using `StewChef`.