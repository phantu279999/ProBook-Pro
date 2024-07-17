function toggleExpand(val_name) {
    var box = document.getElementById(`textBox-${val_name}`);
    console.log(`textBox-${val_name}`);
    console.log(window.getComputedStyle(box).maxHeight);
    if (window.getComputedStyle(box).maxHeight !== '96px') {
        box.style.maxHeight = '96px';
    } else {
        box.style.maxHeight = box.scrollHeight + 'px';
    }
}