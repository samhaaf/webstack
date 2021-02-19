
<script>
  import FormManager from './form_manager.svelte';
  import FormEditor from './form_editor.svelte';
  import FormGenerator from './form_generator.svelte';
  import ObjectEditor from '../utils/object_editor.svelte'
  import DropDown from './inputs/drop_down.svelte'

  let config = {
    'type': 'form',
    // 'items': [
    //   {
    //     'type': 'string',
    //     'name': 'first_name',
    //     'label': 'First name:',
    //     'placeholder': 'Ex. John',
    //     'validations': [],  // default
    //   },{
    //     'type': 'string',
    //     'name': 'last_name',
    //     'label': 'Last name:',
    //     'placeholder': 'Ex. Smith',
    //     'validations': [],  // default
    //   },{
    //     'type': 'reset',
    //   },{
    //     'type': 'submit',
    //   }
    // ]
  }
  let values = {};

  // let options = [1,2,3];
  // let option = 1;
  //
  //
  // async function reset_option() {
  //   await new Promise(resolve => setTimeout(resolve, 3000));
  //   option = 2;
  // }
  //
  // reset_option();

  // $: console.log('fr', values);
  //
  // function reset_values() {
  //   // await new Promise(resolve => setTimeout(resolve, 1000));
  //   config.type = 'poop';
  // }
  //
  // reset_values();



</script>

<FormManager/>
<!-- <DropDown bind:values={options} bind:value={option} null_option={true}/> -->
<!-- <ObjectEditor bind:object={config}/> -->
<!-- <FormEditor bind:config={config} bind:values={values}/> -->
<!-- <FormGenerator {config} /> -->
