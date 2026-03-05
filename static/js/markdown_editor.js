function insertMarkdown(fieldId, startTag, endTag = '') {
    const textarea = document.getElementById(fieldId);
    if (!textarea) return;

    const startPos = textarea.selectionStart;
    const endPos = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(startPos, endPos);

    const replacement = startTag + selectedText + endTag;
    textarea.value = text.substring(0, startPos) + replacement + text.substring(endPos);

    textarea.focus();
    const newCursorPos = (selectedText.length === 0 && endTag.length > 0)
        ? startPos + startTag.length
        : startPos + replacement.length;
    textarea.setSelectionRange(newCursorPos, newCursorPos);
}
