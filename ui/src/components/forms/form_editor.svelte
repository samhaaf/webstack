

<div class='form-view'>

  <h5>Preview</h5>
  <div class='form-container'>
    <FormGenerator bind:raw={raw_html} bind:config={config} bind:values={values}/>
    <!-- {JSON.stringify(config)} -->
  </div>
  <br>

  <h5>Value</h5>
  <ObjectEditor bind:object={values}/>
  <br>

  <h5>Editor</h5>
  <ObjectEditor bind:object={config}/>
  <br>

  <h5>Raw HTML:</h5>
  <div class='raw-container'>
    <div class='code-block-disabled'>{raw_html}</div>
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



<script>
  import FormGenerator from './form_generator.svelte';
  import ObjectEditor from '../utils/object_editor.svelte'

  export let values;
  export let config;

  // to track the html of the form component
  // let cmp;
  // let cmp_html = (document.getElementById('cmp') || {}).outerHTML;
  let raw_html;


  $: console.log('fe values', values);


</script>
