import "../styles/MarkdownContent.css";

function MarkdownContent({ content }) {
  return (
    <div
      className="markdown-content"
      dangerouslySetInnerHTML={{ __html: content }}
    />
  );
}

export default MarkdownContent;