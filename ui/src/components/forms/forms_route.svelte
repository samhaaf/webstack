
<script>
  import FormsExplorer from './forms_explorer.svelte';
  import FormEditor from './form_editor.svelte';
  import FormGenerator from './form_generator.svelte';

  let config = {
    'type': 'form',
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
  }
  let values = {};

  $: console.log('fr', values);

  async function reset_values() {
    await new Promise(resolve => setTimeout(resolve, 5000));
    values = {};
  }
  // reset_values();

</script>


<FormsExplorer/>
<!-- <FormEditor bind:config={config} bind:values={values}/> -->
<!-- <FormGenerator {config} /> -->
