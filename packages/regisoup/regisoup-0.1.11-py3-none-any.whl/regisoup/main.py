import warnings
import typer
from bs4 import BeautifulSoup, Tag
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
import html
import re
import time
import os

MAX_ITER = 100
warnings.simplefilter(action='ignore', category=FutureWarning)


def cookSoup(filename: str) -> BeautifulSoup:
    """Open a file as BeautifulSoup object.

    Will eventually have to be merged with prepareIngredients().

    Args:
        filename: Filename of file to open.
    
    Returns:
        A BeautifulSoup object containing all the contents of that
        file.
    """
    with open(filename) as f:
        soup = BeautifulSoup(f, "html.parser")
    
    return soup


def prepareIngredients(filename: str) -> str:  # Alias convert &lt; and &gt: to < and >
    """Unescape HTML characters.

    This function unescapes HTML characters by saving the file as a decoded file.
    The saved file is made temporary as it is later cleaned up by cleanUpKitchen().
    This function should be deprecated in the future once I get around to merging it
    with cookSoup() as it starts off almost identically as eatSoup().

    Args:
        filename: Filename of file to open.
    
    Returns:
        output_filename: Filename of the temporary unescaped file.
    """

    with open(filename) as f:
        ingredients = f.read()
    
    output_filename = filename.removesuffix(".xml") + str(time.time()) + ".xml"
    with open(output_filename, "w+") as f_out:
        f_out.write(html.unescape(ingredients))

    # Return temp file name, so we can recall it later
    return output_filename

def modifyOpenSoupFigure(soup, caption: bool = True, verbose: bool = False, title: str = None)->int:
    """Finds and replaces <figure> tags.

    This function finds <figure> tags by their child <caption> tags and gets
    things like id, page title and figure file from the tag. The tag is then replaced with the
    new format as described in https://www.mediawiki.org/wiki/Extension:Figures. A quick
    fix for replacing tags that then cease to exist (replace_with did not seem to cooperate) is
    wrap them in dummy tags <p> which are later filtered out and removed by modifyOpenPTags().

    Args:
        soup: BeautifulSoup object that contains the page contents.
        caption: If False will use ID for new figure label.
        verbose: If True will be more verbose.
        title: If given will use given title instead of found page title. Useful in situations, where tags
            don't supply the page's title.
    
    Returns:
        figure_counter: Returns number of modified <figure> tags.
    """
    # Statistics counter
    figure_counter = 0

    for caption_tag in soup.find_all("caption"):
        figure_tag = caption_tag.parent
        
        if verbose:
            print(f"[bold blue]Currently replacing:[/bold blue] {figure_tag}")

        try:
            # Will probably need try and except blocks
            id = figure_tag["id"]
            # Try and find page title (relevant for debug info)
            page = figure_tag.find_previous("title").string
        except AttributeError:
            print(f"[bold red]ERROR![/bold red] :sob: Caught an AttributeError while modifying tag: {figure_tag}")
        
        except KeyError as e:
            print(f"[bold red]ERROR![/bold red] :sob: Caught a KeyError (missing '{e}') while modifying tag: {figure_tag}")
        
        if title:
            page = title
            print(f"[bold red]BUT![/bold red] :smile: A replacement Attribute was provided for: {figure_tag}")

        # If content is len(1) > 1 then raise an exception or warning. NO must wait for [[]] could be on different lines.
        r1 = re.compile("(\n?[\[]).{0}")  # Go look on regexr.com Good page to learn regex
        r2 = re.compile("([\]]).{0}")

        try:
            contents = [content.string for content in figure_tag.contents]
            beginning = list(filter(r1.match, contents))
            end = list(filter(r2.match, contents))
            filtered_content = [beginning[0], end[0]]

            # If label exists; called <caption> it is what should remain of the contents
            label = list(set(contents) - set(filtered_content))
        except Exception:
            print(f"[bold red]ERROR![/bold red] :sob: Caught an exception on page {page}")
            continue

        if caption:
            # Match format of extension Figures https://www.mediawiki.org/wiki/Extension:Figures
            output_string = f"{{{{#figure: |label={id} |content={str(''.join(contents))} }}}}"
        else:
            output_string = f"{{{{#figure: |label={label[0]} |content={str(''.join(filtered_content))} }}}}"

        # Replace the line with the new format!
        clear_text_tag = soup.new_tag("p")
        clear_text_tag.string = output_string
        figure_tag.replace_with(clear_text_tag)
        figure_counter += 1
    
    return figure_counter


def modifyOpenSoupCrossReference(soup, verbose: bool = False, title: str = None):
    """Finds and replaces <xr> tags.

    This function finds <xr> tags by their and gets
    things like id and page title from the tag. The tag is then replaced with the
    new format as described in https://www.mediawiki.org/wiki/Extension:Figures. A quick
    fix for replacing tags that then cease to exist (replace_with did not seem to cooperate) is
    wrap them in dummy tags <p> which are later filtered out and removed by modifyOpenPTags().

    Args:
        soup: BeautifulSoup object that contains the page contents.
        verbose: If True will be more verbose.
        title: If given will use given title instead of found page title. Useful in situations, where tags
            don't supply the page's title.
    
    Returns:
        xr_counter: Returns number of modified <figure> tags.
    """
    # Statistics counter
    xr_counter = 0
    for xr_tag in soup.find_all("xr"):
        page = None
        try:
            id = xr_tag["id"]
            # Find page name up the XML tree
            page = xr_tag.find_previous("title").string
        except AttributeError:
            print(f"[bold red]ERROR![/bold red] :sob: Caught an exception while modifying tag: {xr_tag}")

        except KeyError as e:
            print(f"[bold red]ERROR![/bold red] :sob: Caught a KeyError (missing '{e}') while modifying tag: {xr_tag}")

        if title:
            page = title
            print(f"[bold red]BUT![/bold red] :smile: A replacement Attribute was provided for: {xr_tag}")
        elif page is None:
            print(f"[bold red]CRITICAL![/bold red] :sob: The previous tag is missing a 'title' variable.\
                   \nPlease supply it. For more info read [bold purple]regisoup --help[/bold purple]")
            continue

        output_string = f"{{{{#xref: |page={page} |label={id} }}}}"

        # Replace the line with the new format!
        clear_text_tag = soup.new_tag("p")
        clear_text_tag.string = output_string
        xr_tag.replace_with(clear_text_tag)
        xr_counter += 1

    return xr_counter


def modifyOpenPTags(soup, verbose: bool = False):
    """Finds and replaces dummy <p> tags.

    This function finds dummy <p> tags that are added by modifyOpenSoupFigure() and 
    modifyOpenSoupCrossReference().

    Args:
        soup: BeautifulSoup object that contains the page contents.
        verbose: If True will be more verbose.
    """
    # Might seem counter intuitive to do so many passes of the document but it was 
    # the simplest method I could find.
    p_tags = soup.find_all("p")

    if p_tags is not None:
        for p_tag in p_tags:
            if verbose:
                print(f"[bold blue]Currently replacing:[/bold blue] {p_tag}")

            tag_str = p_tag.string
            if tag_str is None:
                print(f"[bold yellow]Warning![/bold yellow] Dummy <p> tag found but it's supposedly empty. This is unusual behavior.")
                print(f"[bold yellow]Warning![/bold yellow] Attempting to unwrap empty <p> tag.")
                p_tag.unwrap()

            else:
                p_tag.replace_with(tag_str)
    else:
        print(f"[bold yellow]Warning![/bold yellow] No dummy <p> tags found. This is unusual behavior.")



def cleanUpKitchen(filename: str):  # Alias remove temp file
    """Remove temporary converted file.

    This function is used just as a fun alias for os.remove().

    Args:
        filename: Filename of file to remove.
    """
    os.remove(filename)


def eatSoup(output:str, soup, verbose: bool = False, magic: bool = True):  # Alias save file as string
    """Save edited file as encoded file.

    Currently the magic flag is not in use..

    Args:
        output: Filename of file to write output to.
        soup: BeautifulSoup object that contains the page contents.
        verbose: If True will be more verbose.
        magic: If False will not do magic conversion of escaping HTML characters.
    """
    # Save <text> contents as html, the rest as UTF-8 otherwise importDump.php complains.
    if magic:
        for text_tag in soup.find_all("text"):
            # Check through all content. If content is string, escape the HTML 
            # and put it back into the contents. Has to be contents otherwise <ref> tags go away.
            strings = [s for s in text_tag.strings]
            contents = [c for c in text_tag.contents]

            # This loop does dark magic to make sure <ref>'s go where they need to
            for i, content in enumerate(contents):
                if isinstance(content, str):
                    contents[i] = html.escape(content)
                elif isinstance(content, Tag):
                    contents[i] = str(content)
                if verbose:
                    print(f"[bold purple]Currently escaped:[/bold purple] {contents[i]}")

            # This loop should take care of the reqular text
            # for i, string in enumerate(strings):
            #     if isinstance(string, str):
            #         contents[i] = html.escape(string)
            #     
            #         if verbose:
            #             print(f"[bold purple]Currently escaped:[/bold purple] {strings[i]}")

            new_contents = soup.new_string(''.join(contents))
            text_tag.append(new_contents)

    with open(output, "w+") as f:
        f.write(str(soup))


def main(filename: str = typer.Argument(...,help="Filename of file to process, relative to RegiSoup's main.py"), \
         output: str = typer.Argument(...,help="Filename of output file, relative to RegiSoup's main.py"), \
         title: str = typer.Argument(None,help="Specify page title for <xr> tag modification if they do not call it"),\
         caption: bool = typer.Option(True, help = "Keep the figure's found caption. Can result in issues if a figure does not have a caption set"), \
         clean_up: bool = typer.Option(True, help = "Delete temporary files created during processing and HTML decoding"), \
         verbose: bool = typer.Option(False, help = "Print out tags verbatim as they are found"),\
         magic: bool = typer.Option(True, help = "Do deep magic to save encoding of document properly")):
    """
    RegiSoup

    Convert <figure> and <xr> tags from deprecated MediaWiki extension to a new supported format as specified\n
    in the extension Figures available on:
    https://www.mediawiki.org/wiki/Extension:Figures
    """
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task1 = progress.add_task("Preparing soup ingredients (Open file and decode HTML)...", total=1)
        tmp_file = prepareIngredients(filename)
        soup = cookSoup(tmp_file)
        progress.update(task1, advance=1)

        if verbose:
            for tag in soup.find_all(True):
                print(f"[bold purple]Found:[/bold purple] {tag.name}")

        task2 = progress.add_task("Cooking soup (Processing file)...", total=1)
        # Modify file contents and get back counters
        figure_counter = modifyOpenSoupFigure(soup, caption, verbose, title)
        xr_counter = modifyOpenSoupCrossReference(soup, verbose, title)
        modifyOpenPTags(soup, verbose)  # Destroy dummy <p> tags that were added!

        progress.update(task2, advance=1)


        if clean_up:
            task3 = progress.add_task("Cleaning kitchen (Remove temp files)...", total=1)
            cleanUpKitchen(tmp_file)
            progress.update(task3, advance=1)


        task4 = progress.add_task("Eating soup (Saving processed file)...", total=1)
        eatSoup(output, soup, verbose, magic)

        progress.update(task4, advance=1)
        

    # Be verbose about the results
    if figure_counter:
        print(f"[bold green]Success![/bold green] :blush: Found and replaced {figure_counter} <figure> tags.")
    else:
        print(f"[bold yellow]Warning![/bold yellow] :confused: No lines with <figure> were modified.")

    print("\t\t..oh and..\t\t")

    if xr_counter:
        print(f"[bold green]Success![/bold green] :blush: Found and replaced {xr_counter} <xr> tags.")
    else:
        print(f"[bold yellow]Warning![/bold yellow] :confused: No lines with <xr> were modified.")

# if __name__ == "__main__":
#     typer.run(main)
app = typer.run(main)