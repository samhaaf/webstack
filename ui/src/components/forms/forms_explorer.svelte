
<script>
  // import ComponentMap from './component_map.svelte';
  import FormGenerator from './form_generator.svelte';
  // import { JSONEditor } from 'svelte-jsoneditor';
  // import AceEditor from '../utils/ace_editor.svelte';

  let cmp;
  let cmp_html;
  let form_name = 'test_form';
  let values;
  let config = {
    'type': 'form',
    'name': 'test-form',
    'version': 'v0.1',
    'items': [
      {
        'type': 'string',
        'name': 'first_name',
        'label': 'First name:',
        'placeholder': 'Ex. John',
        'validations': [],  // default
      },{
        'type': 'string',
        'name': 'last_name',
        'label': 'Last name:',
        'placeholder': 'Ex. Smith',
        'validations': [],  // default
      },{
        'type': 'reset',
      },{
        'type': 'submit',
      }
    ]
  };

  $: console.log('values:', values);


  $: if (cmp != null) {
    cmp_html = document.getElementById('cmp').outerHTML;
  }

  // make config editable as a string
  let config_string = JSON.stringify(config, null, 2);
  let config_is_error = false;
  $: if (config_string) {
    try {
      config = JSON.parse(config_string)
      config_is_error = false;
    }
    catch (error) {
      config_is_error = true;
    }
  }

</script>


<div class='form-explorer'>
<!--
  <p>Form: {config.name}</p>
  <p>Version: {config.name}</p>
  <br><br> -->

  <h4>Form</h4>
  <div class='form-container'>
    <FormGenerator bind:this={cmp} config={config} bind:values={values} id="cmp" />
    <!-- {JSON.stringify(config)} -->
  </div>
  <br><br>

  <h4>Form Value</h4>
  <div class='value-container' >
    <!-- <AceEditor value={JSON.stringify(config)} lang="json"/> -->
    <pre><code>
      <div contenteditable class="code-block">
        {JSON.stringify(values)}
      </div>
    </code></pre>
  </div>
  <br><br>

  <h4>Form Editor</h4>
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

  <h4>Raw Form HTML:</h4>
  <div class='code-block-disabled'>{cmp_html}</div>

</div>


<style>
  .form-explorer {
    border: 2px outset;
    margin: 6px;
    padding: 6px;
  }
  .editor-container {
    margin: 12px;
    /* width: calc(100% - 12px); */
  }
  .editor-container > div[contenteditable] {
    width: 100%;
  }
  .form-container {
    margin: 12px;
    padding: 12px;
    border: 2px inset;
    background-color: var(--pallete-0);
    /* background-color: rgba(35, 194, 137, 0.35); */
  }
  .json-parse-error {
    /* border: 2px inset red; */
    background-color: lightyellow;
  }

</style>
