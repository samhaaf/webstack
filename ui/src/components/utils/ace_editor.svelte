<script>
  import { createEventDispatcher, tick, onMount, onDestroy } from "svelte";
  import * as ace from "brace";
  import "brace/ext/emmet";
  const EDITOR_ID = `svelte-ace-editor-div:${Math.floor(Math.random() * 10000000000)}`;
  // const dispatch = createEventDispatcher<{
  //   init: ace.Editor;
  //   input: string;
  //   selectionChange: any;
  //   blur: void;
  //   changeMode: any;
  //   commandKey: { err: any; hashId: any; keyCode: any };
  //   copy: void;
  //   cursorChange: void;
  //   cut: void;
  //   documentChange: { data: any };
  //   focus: void;
  //   paste: string;
  // }>();
  const dispatch = createEventDispatcher();

  /**
   * translation of vue component to svelte:
   * @link https://github.com/chairuosen/vue2-ace-editor/blob/91051422b36482eaf94271f1a263afa4b998f099/index.js
   **/
  export let value = ""; // String, required
  export let lang = "json"; // String
  export let theme = "chrome"; // String
  export let height = "100%"; // null for 100, else integer, used as percent
  export let width = "100%"; // null for 100, else integer, used as percent
  export let options = {}; // Object

  let editor = ace.Editor;
  let contentBackup = "";

  const requireEditorPlugins = () => {};
  requireEditorPlugins();

  onDestroy(() => {
    if (editor) {
      editor.destroy();
      editor.container.remove();
    }
  });

  $: watchValue(value);
  function watchValue(val) {
    if (contentBackup !== val && editor && typeof val === "string") {
      editor.session.setValue(val);
      contentBackup = val;
    }
  }

  $: watchTheme(theme);
  function watchTheme(newTheme) {
    if (editor) {
      editor.setTheme("ace/theme/" + newTheme);
    }
  }

  $: watchMode(lang);
  function watchMode(newOption) {
    if (editor) {
      editor.getSession().setMode("ace/mode/" + newOption);
    }
  }

  $: watchOptions(options);
  function watchOptions(newOption) {
    if (editor) {
      editor.setOptions(newOption);
    }
  }

  const resizeOnNextTick = () =>
    tick().then(() => {
      if (editor) {
        editor.resize();
      }
    });

  $: if (height !== null && width !== null) {
    resizeOnNextTick();
  }

  onMount(() => {
    lang = lang || "text";
    theme = theme || "chrome";

    editor = ace.edit(EDITOR_ID);

    dispatch("init", editor);
    editor.$blockScrolling = Infinity;
    // editor.setOption("enableEmmet", true);
    editor.getSession().setMode("ace/mode/" + lang);
    editor.setTheme("ace/theme/" + theme);
    editor.setValue(value, 1);
    contentBackup = value;
    setEventCallBacks();
    if (options) {
      editor.setOptions(options);
    }
  });

  const ValidPxDigitsRegEx = /^\d*$/;
  function px(n) {
    if (ValidPxDigitsRegEx.test(n)) {
      return n + "px";
    }
    return n;
  }

  function setEventCallBacks() {
    editor.onBlur = () => dispatch("blur");
    editor.onChangeMode = (obj) => dispatch("changeMode", obj);
    editor.onCommandKey = (err, hashId, keyCode) =>
      dispatch("commandKey", { err, hashId, keyCode });
    editor.onCopy = () => dispatch("copy");
    editor.onCursorChange = () => dispatch("cursorChange");
    editor.onCut = () => dispatch("cut");
    editor.onDocumentChange = (obj) =>
      dispatch("documentChange", obj);
    editor.onFocus = () => dispatch("focus");
    editor.onPaste = (text) => dispatch("paste", text);
    editor.onSelectionChange = (obj) => dispatch("selectionChange", obj);
    editor.on("change", function () {
      const content = editor.getValue();
      value = content;
      dispatch("input", content);
      contentBackup = content;
    });
  }
</script>

<div id={EDITOR_ID} style="width:{px(width)};height:{px(height)}" />
