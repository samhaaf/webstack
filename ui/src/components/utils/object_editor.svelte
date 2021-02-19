

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
  $: if ('disabled' in $$props) {
    disabled = $$props.disabled === null ? true : $$props.disabled
  }

  let lock_id;
  let editor_string;
  let editor_cached;
  let object_cached;
  let parse_error = false;

  // $: console.log('lock_id', lock_id);

  // async function to trick compiler to ignore circular reference
  async function rebuild_object() {
    let my_lock = Date.now();
    lock_id = my_lock
    if (editor_string != editor_cached) {
      try {
        object = deserialize(editor_string.replaceAll(/<\/?[^>]+>/gi, ''))
        // console.log('updated', object);
        parse_error = false;
        // await sleep(100)
      }
      catch (error) {
        parse_error = true;
        // console.log('error');
      }
    } else {
      parse_error = false;
    }
    if (lock_id == my_lock) {
      lock_id = null
    }
    if (lock_id == null && !parse_error) {
      editor_cached = editor_string
      // console.log('cached');
    }
  }

  // on object updates, reset the string
  $: if (object) {
    if (object_cached != object && lock_id == null) {
      // console.log('oe', object);
      // console.log({lock_id});
      editor_string = serialize(object, 2);
      editor_cached = editor_string;
      object_cached = Object.assign(object);
    }
  }

  $: if (editor_string) {
    // console.log('rebuilding', editor_string, editor_cached);
    rebuild_object()
  }


  // // async function to trick compiler to ignore circular reference
  // async function reset_editor_string() {
  //   await sleep(100)
  //   editor_string = serialize(object, 2)
  // }


</script>
