from sys import argv
import convert, copytree, os


def main():
    basepath = get_basepath()
    copytree.copy_source_to_build()
    generate_pages_recursive("content", "template.html", "public")

def get_basepath():
    if argv[1]:
        basepath = argv[1]
    else:
        basepath = "/"
    return basepath

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}.\n")

    if os.path.isfile(from_path):
        with open(from_path) as file:
            markdown = file.read()

    if os.path.isfile(template_path) and template_path.endswith(".html"):
        with open(template_path) as file:
            template = file.read()

    node = convert.markdown_to_html_node(markdown)
    html = node.to_html()
    title = convert.extract_title(markdown)

    output = template.replace("{{ Title }}", title)
    output = output.replace("{{ Content }}", html)
    output = template.replace('href="/', 'href="' + basepath)
    output = template.replace('src="/', 'src="' + basepath)

    with open(dest_path, "w") as file:
        file.write(output)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath:str):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_path.replace(".md", ".html"))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path, basepath)



if __name__ == "__main__":
    main()