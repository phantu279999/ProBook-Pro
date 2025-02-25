function toggleExpand(valName) {
    const box = document.getElementById(`textBox-${valName}`);
    const currentMaxHeight = box.style.maxHeight || window.getComputedStyle(box).maxHeight;

    if (currentMaxHeight !== '96px') {
        box.style.maxHeight = '96px';
    } else {
        box.style.maxHeight = `${box.scrollHeight}px`;
    }
}