

<div class='editor-container' >
  <!-- <AceEditor value={editor_string} lang="json"/> -->
  <pre><code>
    <div contenteditable
      class={"code-block" + (parse_error ? ' parse-error' : '')}
      bind:innerHTML={editor_string}
    />
  </code></pre>
</div>



<style>
  .editor-container {
    /* margin: 12px; */
    padding: 12px;
    /* max-width: 600px; */
  }
  .parse-error {
    border: 2px inset red;
    background-color: lightyellow;
  }
</style>



<script>
  import { sleep } from './time.js';
  import { serialize, deserialize } from './serde.js';
  // TODO: import AceEditor from '../utils/ace_editor.svelte';

  export let object;

  // TODO allow <... {style}> syntax
  // TODO allow <... disabled> syntax
  let disabled = false;
  $: if ('disabled' in $$props) { disabled = $$props.disabled === null ? true : $$props.disabled }


  // make config editable as a string
  let editor_string;
  let parse_error = false;
  $: if (editor_string) {
    try {
      object = deserialize(editor_string.replaceAll(/<\/?[^>]+>/gi, ''))
      parse_error = false;
    }
    catch (error) {
      parse_error = true;
    }
  }

  // async function to trick compiler to ignore circular reference
  async function reset_editor_string() {
    await sleep(100)
    editor_string = serialize(object, 2)
  }

  // on object updates, reset the string
  $: if (object) {
    reset_editor_string()
  }

</script>
