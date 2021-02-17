
<script>
  import FormGenerator from './form_generator.svelte';
  // import { Collapse } from 'svelma';
  // import AceEditor from '../utils/ace_editor.svelte';

  export let values;
  export let config;

  // to track the html of the form component
  let cmp;
  let cmp_html = (document.getElementById('cmp') || {}).outerHTML;

  async function sleep(ms) {await new Promise(resolve => setTimeout(resolve, ms))}

  // make config editable as a string
  let config_string = JSON.stringify(config, null, 2);
  let config_is_error = false;
  $: if (config_string) {
    try {
      config = JSON.parse(config_string.replace(/<\/?[^>]+>/gi, ''))
      config_is_error = false;
    }
    catch (error) {
      config_is_error = true;
    }
  }
  // function to trick compiler to ignore circular reference
  async function reset_config_string() {
    await sleep(100)
    config_string = JSON.stringify(config, null, 2)
  }
  $: if (config) {
    reset_config_string()
  }


  // make values editable as a string
  let values_string = JSON.stringify(values, null, 2);
  let values_is_error = false;
  $: if (values_string) {
    try {
      values = JSON.parse(values_string.replace(/<\/?[^>]+>/gi, ''))
      values_is_error = false;
    }
    catch (error) {
      values_is_error = true;
    }
  }
  // function to trick compiler to ignore circular reference
  async function reset_values_string() {
    await sleep(100)
    values_string = JSON.stringify(values, null, 2)
  }
  $: if (values) {
    reset_values_string()
  }

  $: if (config || values) {
    const update_html = async () => {
      await sleep(100)
      cmp_html = (document.getElementById('cmp') || {}).outerHTML;
    }
    update_html()
  }

  $: console.log('fe values', values);


</script>

<!--
  <p>Form: {config.name}</p>
  <p>Version: {config.name}</p>
  <br><br> -->


<div class='form-view'>

  <h3>Form</h3>
  <div class='form-container'>
    <FormGenerator bind:this={cmp} bind:config={config} bind:values={values} id="cmp" />
    <!-- {JSON.stringify(config)} -->
  </div>
  <br><br>

  <!-- <Collapse> -->
    <h5>Value</h5>
    <div class='value-container' id='value-container' >
      <!-- <AceEditor value={JSON.stringify(config)} lang="json"/> -->
      <pre><code>
        <div contenteditable
          class={"code-block" + (values_is_error ? ' json-parse-error' : '')}
          bind:innerHTML={values_string}
          > <!-- contenteditable -->

        </div>
      </code></pre>
    </div>
  <!-- </Collapse> -->
  <br><br>

  <h5>Editor</h5>
  <div class='editor-container' >
    <!-- <AceEditor value={JSON.stringify(config)} lang="json"/> -->
    <pre><code>
      <div
        contenteditable
        class={"code-block" + (config_is_error ? ' json-parse-error' : '')}
        bind:innerHTML={config_string}
      />
    </code></pre>
  </div>
  <br><br>

  <h5>Raw HTML:</h5>
  <div class='raw-container'>
    <div class='code-block-disabled'>{cmp_html}</div>
  </div>

</div>

<style>
  .form-view {
    border: 2px outset;
    margin: 12px;
    padding: 6px;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }
  .form-container {
    margin: 12px;
    padding: 12px;
    border: 2px inset;
    /* background-color: var(--pallete-0); */
    max-width: 600px;
    /* background-color: rgba(35, 194, 137, 0.35); */
  }
  .value-container {
    margin: 12px;
    background-color: var(--pallete-0);
    max-width: 600px;
  }
  .editor-container {
    margin: 12px;
    max-width: 600px;
  }
  .raw-container {
    margin: 12px;
    max-width: 600px;
  }
  .json-parse-error {
    /* border: 2px inset red; */
    background-color: lightyellow;
  }
</style>
