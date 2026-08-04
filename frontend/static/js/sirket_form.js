/* sirket_form.js — sunucu doğrulaması sonrası ilk hatalı alana odaklan */
document.addEventListener("DOMContentLoaded", function () {
  const hatali = document.querySelector(".is-invalid");
  if (hatali) {
    hatali.scrollIntoView({ behavior: "smooth", block: "center" });
    hatali.focus({ preventScroll: true });
  }

  const fileInput = document.querySelector("#attachments");
  const fileDrop = document.querySelector("[data-file-drop]");
  const selectedPanel = document.querySelector("[data-selected-files]");
  if (fileInput && fileDrop && selectedPanel) {
    const selectedList = selectedPanel.querySelector("[data-selected-files-list]");
    const selectedTitle = selectedPanel.querySelector("[data-selected-files-title]");
    const status = selectedPanel.querySelector("[data-file-status]");
    const clearButton = selectedPanel.querySelector("[data-files-clear]");
    const dropIcon = fileDrop.querySelector("[data-file-drop-icon]");
    const dropTitle = fileDrop.querySelector("[data-file-drop-title]");
    const dropCopy = fileDrop.querySelector("[data-file-drop-copy]");
    const canManageFiles = typeof DataTransfer === "function";
    const maximumFiles = 10;
    const maximumFileSize = 100 * 1024 * 1024;
    let selectedFiles = [...fileInput.files];

    function formatFileSize(bytes) {
      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }

    function fileKey(file) {
      return `${file.name}:${file.size}:${file.lastModified}`;
    }

    function syncInputFiles() {
      if (!canManageFiles) return;
      const transfer = new DataTransfer();
      selectedFiles.forEach((file) => transfer.items.add(file));
      fileInput.files = transfer.files;
    }

    function renderFiles(message = "") {
      selectedList.replaceChildren();
      selectedFiles.forEach((file, index) => {
        const item = document.createElement("li");
        const icon = document.createElement("i");
        const details = document.createElement("div");
        const name = document.createElement("strong");
        const size = document.createElement("span");
        const remove = document.createElement("button");

        icon.className = "bi bi-file-earmark-check";
        icon.setAttribute("aria-hidden", "true");
        name.textContent = file.name;
        size.textContent = formatFileSize(file.size);
        details.append(name, size);
        remove.type = "button";
        remove.dataset.fileRemove = String(index);
        remove.setAttribute("aria-label", `${file.name} dosyasını seçimden kaldır`);
        remove.innerHTML = '<i class="bi bi-x-lg" aria-hidden="true"></i>';
        if (!canManageFiles) remove.hidden = true;
        item.append(icon, details, remove);
        selectedList.appendChild(item);
      });

      const count = selectedFiles.length;
      const totalSize = selectedFiles.reduce((sum, file) => sum + file.size, 0);
      selectedPanel.hidden = count === 0 && !message;
      fileDrop.classList.toggle("file-drop-selected", count > 0);
      dropIcon.className = count
        ? "bi bi-check2-circle"
        : "bi bi-cloud-arrow-up";
      dropTitle.textContent = count
        ? `${count} dosya seçildi`
        : "Dosya seçin";
      dropCopy.textContent = count
        ? "Dosya eklemek için yeniden tıklayın"
        : "Bir veya birden fazla belge, fotoğraf ya da video";
      selectedTitle.textContent = `Seçilen dosyalar (${count}/10)`;
      status.textContent = message || (
        count ? `Toplam boyut: ${formatFileSize(totalSize)}` : ""
      );
      status.classList.toggle("selected-files-warning", Boolean(message));
      clearButton.hidden = count === 0;
    }

    function addFiles(files) {
      if (!canManageFiles) {
        selectedFiles = [...files];
        renderFiles();
        return;
      }

      const existingKeys = new Set(selectedFiles.map(fileKey));
      let duplicateCount = 0;
      let oversizedCount = 0;
      let limitCount = 0;
      [...files].forEach((file) => {
        if (existingKeys.has(fileKey(file))) {
          duplicateCount += 1;
          return;
        }
        if (file.size > maximumFileSize) {
          oversizedCount += 1;
          return;
        }
        if (selectedFiles.length >= maximumFiles) {
          limitCount += 1;
          return;
        }
        selectedFiles.push(file);
        existingKeys.add(fileKey(file));
      });
      syncInputFiles();

      const messages = [];
      if (oversizedCount) messages.push(`${oversizedCount} dosya 100 MB sınırını aştığı için eklenmedi.`);
      if (limitCount) messages.push(`En fazla ${maximumFiles} dosya seçilebilir.`);
      if (duplicateCount) messages.push(`${duplicateCount} yinelenen dosya tekrar eklenmedi.`);
      renderFiles(messages.join(" "));
    }

    fileInput.addEventListener("change", function () {
      addFiles(fileInput.files);
    });

    selectedList.addEventListener("click", function (event) {
      const remove = event.target.closest("[data-file-remove]");
      if (!remove || !canManageFiles) return;
      selectedFiles.splice(Number(remove.dataset.fileRemove), 1);
      syncInputFiles();
      renderFiles();
    });

    clearButton.addEventListener("click", function () {
      selectedFiles = [];
      fileInput.value = "";
      syncInputFiles();
      renderFiles();
      fileInput.focus();
    });

    if (canManageFiles) {
      ["dragenter", "dragover"].forEach((eventName) => {
        fileDrop.addEventListener(eventName, function (event) {
          event.preventDefault();
          fileDrop.classList.add("file-drop-active");
        });
      });
      ["dragleave", "drop"].forEach((eventName) => {
        fileDrop.addEventListener(eventName, function (event) {
          event.preventDefault();
          fileDrop.classList.remove("file-drop-active");
        });
      });
      fileDrop.addEventListener("drop", function (event) {
        addFiles(event.dataTransfer.files);
      });
    }
    renderFiles();
  }

  const editor = document.querySelector("[data-instrument-editor]");
  if (!editor) return;

  const rowsContainer = editor.querySelector("[data-instrument-rows]");
  const template = editor.querySelector("[data-instrument-template]");
  const addButton = editor.querySelector("[data-instrument-add]");
  const totalOutput = editor.querySelector("[data-instrument-total]");
  let controlSequence = rowsContainer.querySelectorAll("[data-instrument-row]").length;

  function rows() {
    return [...rowsContainer.querySelectorAll("[data-instrument-row]")];
  }

  function updateEditor() {
    const currentRows = rows();
    let total = 0;
    const selectedKinds = currentRows
      .map((row) => row.querySelector('select[name="olcu_aleti_cinsi"]').value)
      .filter(Boolean);

    currentRows.forEach((row, index) => {
      const select = row.querySelector('select[name="olcu_aleti_cinsi"]');
      const quantity = row.querySelector('input[name="olcu_aleti_sayisi"]');
      const remove = row.querySelector("[data-instrument-remove]");
      const ownValue = select.value;

      row.querySelectorAll("label").forEach((label) => {
        const control = label.nextElementSibling;
        if (!control) return;
        if (!control.id) control.id = `instrument-control-${controlSequence++}`;
        label.htmlFor = control.id;
      });
      row.dataset.rowNumber = String(index + 1);
      remove.hidden = currentRows.length === 1;

      [...select.options].forEach((option) => {
        option.disabled = Boolean(
          option.value
          && option.value !== ownValue
          && selectedKinds.includes(option.value)
        );
      });

      const number = Number.parseInt(quantity.value, 10);
      if (Number.isInteger(number) && number > 0) total += number;
    });

    totalOutput.textContent = `Toplam ölçü aleti: ${total}`;
    addButton.disabled = currentRows.length >= 50;
  }

  addButton.addEventListener("click", function () {
    if (rows().length >= 50) return;
    const fragment = template.content.cloneNode(true);
    const newRow = fragment.querySelector("[data-instrument-row]");
    rowsContainer.appendChild(fragment);
    updateEditor();
    newRow.querySelector("select").focus();
  });

  rowsContainer.addEventListener("click", function (event) {
    const remove = event.target.closest("[data-instrument-remove]");
    if (!remove || rows().length === 1) return;
    remove.closest("[data-instrument-row]").remove();
    updateEditor();
  });

  rowsContainer.addEventListener("input", updateEditor);
  rowsContainer.addEventListener("change", updateEditor);
  updateEditor();
});
