import subprocess, os
import typer
from bs4 import BeautifulSoup
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.pretty import pprint
import tomli
import requests
import time
from difflib import Differ

MAX_ITER = 10000
app = typer.Typer()

def login(URL, USER, PASSWORD):
    """Logs bot into the Wiki's API.

    This function sends a GET request for a login token and further on
    a POST request with the bots Username and Password to the URL set in config.toml.
    All arguments for this function are set in the config.toml file by default.
    It gets back the active session and CSRF_TOKEN which is required for page
    modification.

    Args:
        URL: URL of the Wiki's API endpoint.
        USER: Username of the bot.
        PASSWORD: Password of the bot.

    Returns:
        S: Active session object to send GET/POST requests to.
        CSRF_TOKEN: A token needed to be given when modifying pages.
    """
    S = requests.Session()

    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }
    R = S.get(URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]

    PARAMS_1 = {
        "action": "login",
        "lgname": USER,
        "lgpassword": PASSWORD,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }

    R = S.post(URL, data=PARAMS_1)

    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(URL, params=PARAMS_2)
    DATA = R.json()
    CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]

    if CSRF_TOKEN == "+\\":
        print(f"[bold red]ERROR![/bold red] Could not log in.. Check credentials for [bold yellow]{URL} [/bold yellow]")
        raise typer.Exit()

    return S, CSRF_TOKEN


def retrievePagePacket(prev_continue, URL, S, verbose:bool = False):
    """Get a packet of pages with their matching titles.

    Will query the Wiki API endpoint for all pages via the 'allpages' generator.
    This generator only returns packets of about 10 pages or so, so multiple queries
    are needed to get all pages. This function is called multiple times in a while True
    loop from inside feast() which is where that is done so. This function does not
    however get their contents, only their titles.

    Args:
        prev_continue: A token returned by the previous call of the generator. 
            Is an empty dictionary for first iteration.
        URL: URL of the Wiki's API endpoint.
        S: Active session object to send GET/POST requests to.
        verbose: If True be more verbose.
    
    Returns:
        ALL_PAGE_DATA: Direct data given from GET request 
        prev_continue: A token returned by the previous call of the generator.
    """
    PARAMS = {
        "action": "query",
        "generator": "allpages",
        "gapcontinue": prev_continue,
        "format": "json"
    }

    R = S.get(URL, params=PARAMS)
    ALL_PAGE_DATA = R.json()

    if verbose:
        print(ALL_PAGE_DATA)

    try:
        prev_continue = ALL_PAGE_DATA["continue"]["gapcontinue"]
    except KeyError:
        # This should be handled in the main() function inside the exit condition
        # of the while True block
        pass
    if verbose:
        print(prev_continue)

    return ALL_PAGE_DATA, prev_continue


def modifyPagePacket(ALL_PAGE_DATA, CSRF_TOKEN, URL, S, regisoup_out: bool = False, commit: bool= False, diff: bool = False):
    """Take a packet of pages and run them through RegiSoup.

    This function gets the contents of a packet of pages by each
    individual pages title. It then parses the page contents through 
    RegiSoup via a temporary file and returns the edited contents. If the
    commit flag is set, then changes are pushed to the API endpoint via a
    POST request. A CSRF_TOKEN is needed to commit the changes. It can be
    the same token for all the changes.

    Args:
        ALL_PAGE_DATA: Direct data (JSON object) given from GET request to 
            to the API endpoint called in retrievePagePacket().
        CSRF_TOKEN: Token gotten from login. Needed to commit changes to Wiki.
        URL: URL of the Wiki's API endpoint.
        S: Active session object to send GET/POST requests to.
        regisoup_out: If true, log the output of RegiSoup to stdout.
        commit: If true, commit changes to the Wiki.
        diff: If true, create a directory diff/ and fill it with diff files for
            each page to be modified. Each title corresponds to one page and a
            delta difference between the modified and unmodified version is given.
        
    Returns:
        pages_edited: Number of pages that were edited and had those edits
            committed to the Wiki.
    
    """
    # Statistics counters
    pages_edited = 0

    # For every page title
    for page in ALL_PAGE_DATA["query"]["pages"]:
        page_data = ALL_PAGE_DATA["query"]["pages"][page]
        page_title = page_data["title"]

        # Get page contents by title
        PARAMS = {
            "action": "parse",
            "page": page_title,
            "prop": "wikitext",
            "format": "json"
        }

        R = S.get(URL, params=PARAMS)
        PAGE_DATA = R.json()
        page_contents = PAGE_DATA["parse"]["wikitext"]["*"]

        # RegiSoup explicitly searches for <caption> blocks and then finds parent <figure> tags
        # since it expects all content to be wrapped in tags we wrap it in arbitrary tags
        soup = BeautifulSoup("<arbitrary>" + page_contents + "</arbitrary>", features="lxml")

        if not os.path.exists("tmp"):
                os.makedirs("tmp")

        with open("tmp/tmp_storage.txt", "w+") as f:
            input = str(soup)
            f.write(input)

        print(f"[bold yellow]RegiSoup[/bold yellow] :innocent: is cooking {page_title}")

        # Send page contents to RegiSoup
        bashCommand = f"regisoup tmp/tmp_storage.txt  tmp/tmp_out.txt \"{page_title}\""

        bash_output = subprocess.run(bashCommand, shell=True, capture_output=True)
        if bash_output.stderr:
            print(f"[bold red]CRITICAL![/bold red] Encountered exception on page {page_title}!")
            if regisoup_out:
                print(f"[bold red]{bash_output.stderr.decode()}")

        if regisoup_out:
            print(bash_output.stdout.decode())

        with open("tmp/tmp_out.txt") as f:
            output = f.read()
            soup = BeautifulSoup(output, features="xml")

        # Unwrap all the dummy tags we've added
        soup.html.unwrap()
        soup.body.unwrap()
        soup.arbitrary.unwrap()
        page_contents = str(soup).removeprefix("<?xml version=\"1.0\" encoding=\"utf-8\"?>")

        # Send edit request to MediaWiki API
        PARAMS = {
            "action": "edit",
            "token": CSRF_TOKEN,
            "title": page_title,
            "text": page_contents,
            "format": "json"
        }


        if diff:
            d = Differ()
            delta = ''.join(list(d.compare(input.splitlines(keepends=True), output.splitlines(keepends=True))))

            delta_file = f"diff/{page_title.replace(' ', '')}.diff"

            # Create the file path if it does not yet exist
            if not os.path.exists("diff"):
                os.makedirs("diff")

            try:
                # Write the diff to a file
                with open(delta_file, "w+") as f:
                    f.write(delta)
            except FileNotFoundError:
                print(f"[bold red]ERROR! [/bold red]Could not generate diff file for {page_title}")


        if commit:
            print(f"[bold purple]Now modifying:[/bold purple] :no_mouth: {page_title}")
            S.post(URL, data=PARAMS)
            pages_edited += 1

    return pages_edited

@app.command()
def feast(config_path: str = typer.Argument("config.toml", help="Filename of config file, relative to RegiSoup's main.py"),
         verbose: bool = typer.Option(False, help = "Be more verbose"),
         commit: bool = typer.Option(False, help = "Commit changes to the live wikipedia API endpoint"),
         diff: bool = typer.Option(False, help = "Get diff after conversion. Output in diff/"),
         regisoup_out: bool = typer.Option(False, help = "Print out RegiSoup responses"),
         dry_run: bool = typer.Option(False, help = "Only retrieve pages but don't send them to RegiSoup")):
    """
    StewChef: Feast-size serving

    MASS retrieve all the pages on the Wiki and state modifications by RegiSoup. If specified, changes
    will be committed to the Wiki given at the API endpoint
    """
    # Statistics counters
    total_pages_edited = 0

    # Read config.toml
    with open(config_path, "rb") as f:
        config = tomli.load(f)

    URL = config["server"]["url"]

    USER = config["bot"]["user"]
    PASSWORD = config["bot"]["password"]

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task1 = progress.add_task("Logging in..", total=1)
        S, CSRF_TOKEN = login(URL, USER, PASSWORD)
        progress.update(task1, advance=1)

        if commit:
            task2 = progress.add_task("Retrieving and modifying pages..", total=1)
        else:
            task2 = progress.add_task("Retrieving pages..", total=1)
        prev_continue = {}
        iter_counter = 0
        while True:
            ALL_PAGE_DATA, prev_continue = retrievePagePacket(prev_continue, URL, S, verbose)

            if not dry_run:
                total_pages_edited += modifyPagePacket(ALL_PAGE_DATA, CSRF_TOKEN, URL, S, regisoup_out, commit, diff)

            # Sleep so we don't spam the server with requests
            time.sleep(0.2)
            iter_counter += 1

            # Exit condition from retrievePagePacket() handled here
            if "continue" not in ALL_PAGE_DATA or iter_counter >= MAX_ITER:
                break

        progress.update(task2, advance=1)

        if commit:
            print(f"[bold green]Success![/bold green] Retrieved and modified {total_pages_edited} pages :blush:")
        elif dry_run:
            print(f"[bold green]Done recieving pages :blush:[/bold green]")
        elif diff:
            print(f"[bold green]Success![/bold green] Generated diff files :blush:")
        else:
            print(f"[bold green]Success![/bold green] I have done nothing, because you haven't specified any flags :upside__down_face:")


@app.command()
def single(page_title: str = typer.Argument(...,help="Filename of output file, relative to RegiSoup's main.py"),
           config_path: str = typer.Argument("config.toml", help="Filename of config file, relative to RegiSoup's main.py"),
           verbose: bool = typer.Option(False, help = "Be more verbose"),
           save: bool = typer.Option(False, help = "Save requested file"),
           save_path: str = typer.Argument(None, help="Path of file to save requested page"),
           as_html: bool = typer.Option(False, help = "Save file as HTML document")):
    """
    StewChef: Single Serving

    Retrieve, modify and, if specified, save a single page of the Wiki
    given at the API endpoint by the Wiki page's title.
    """
    print("[bold blue]Cooking up a single serving![/bold blue]")
    # Read config.toml
    try:
        with open(config_path, "rb") as f:
            config = tomli.load(f)
    except FileNotFoundError:
        print(f"[bold red]ERROR![/bold red] Config file not found.. Read the documentation for more information.")
        raise typer.Exit()

    URL = config["server"]["url"]

    USER = config["bot"]["user"]
    PASSWORD = config["bot"]["password"]

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task1 = progress.add_task("Logging in..", total=1)
        S, CSRF_TOKEN = login(URL, USER, PASSWORD)
        progress.update(task1, advance=1)

        task2 = progress.add_task("Requesting page..", total=1)
        PARAMS = {
            "action": "parse",
            "page": page_title,
            "prop": "wikitext",
            "format": "json"
        }

        R = S.get(URL, params=PARAMS)
        DATA = R.json()
        try:
            page_contents = DATA["parse"]["wikitext"]["*"]
        except KeyError:
            print(f"[bold red]ERROR![/bold red] Page titled [purple]{page_title}[/purple] not found!")
            raise typer.Exit()  # Exit the program

        progress.update(task2, advance=1)

        if verbose:
            print(DATA)
        else:
            pprint(page_contents)

        if save:
            # WARNING: IMPORTANT STEP!
            # Set save_path from None to title

            if save_path is None:
                save_path = page_title.replace(" ", "")

            if as_html:
                with open(save_path, "w+") as f:
                    f.write(str(BeautifulSoup(page_contents, features="lxml")))
            else:
                with open(save_path, "w+") as f:
                    f.write(page_contents)



# if __name__ == "__main__":
#     app()
