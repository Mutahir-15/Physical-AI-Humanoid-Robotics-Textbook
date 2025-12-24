import re

def clean_mdx_content(mdx_content: str) -> str:
    """
    Cleans MDX content by removing Docusaurus-specific syntax,
    comments, and potentially converting some Markdown to plain text.
    """
    # Remove Docusaurus <Tabs> and <TabItem> components and their content
    mdx_content = re.sub(r"<Tabs>.*?</Tabs>", "", mdx_content, flags=re.DOTALL)
    mdx_content = re.sub(r"<TabItem.*?>.*?</TabItem>", "", mdx_content, flags=re.DOTALL)
    
    # Remove comments
    mdx_content = re.sub(r"<!--.*?-->", "", mdx_content, flags=re.DOTALL)
    
    # Remove any remaining JSX-like tags (e.g., <CustomComponent />)
    mdx_content = re.sub(r"<[^>]+?>", "", mdx_content)
    
    # Convert Markdown links to just their text
    mdx_content = re.sub(r"[(.*?)](.*?)","\1", mdx_content)
    
    # Remove images (keep alt text if present)
    mdx_content = re.sub(r"![(.*?)](.*?)","\1", mdx_content)

    # Basic conversion of headings to plain text (e.g., '## Heading' -> 'Heading')
    mdx_content = re.sub(r"^[#]+\s*(.*)", "\1", mdx_content, flags=re.MULTILINE)

    # Normalize whitespace
    mdx_content = re.sub(r"\s+", " ", mdx_content).strip()
    return mdx_content
