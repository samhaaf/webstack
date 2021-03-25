
<div class='form-route pallete-0 tile'>
  <h2>Forms</h2>
  <p>
    This collection of tools are designed to generate and manage user interfaces,
    a.k.a. forms. As with the other tools demonstrated on this site, every
    component is designed to work in a standalone context, but can be bound with
    neighboring components to create more complex applications.
  </p>
  <br><br>


  <div class='card'>
    <div class='card-header'>Form Manager</div>
    <!-- <div class='card-image'>
      <img src='static/images/FormManager.png' alt='An image of the FormGenerator.'/>
    </div> -->
    <div class='card-body'>
      This dashboard tool provides an explorative interface to a collection of
      forms for an application or client(s).

      <br><br><br>
      <img src='static/images/FormManager.png' alt='An image of the FormGenerator.'/>

      <br><br><br>
      <h5>Current Features:</h5>
      <ul>
        <li>Create new forms and form versions</li>
        <li>View live preview of form</li>
        <li>See and edit live form values with reactive editor</li>
        <ul>
          <li>Embeded JavaScipt functions
        </ul>
        <li>See and edit live form values with reactive editor</li>
        <li>Browser caching for change persistance</li>
      </ul>

      <br><br>
      <h5>Roadmap:</h5>
      <ul>
        <li>Create more exhaustive collection of inputs for all datatypes</li>
        <li>Graphical configuration builder (point and click)</li>
        <li>Configuration syntax for links to other forms</li>
        <li>Configuration syntax for database pipelines</li>
        <li>Form validation</li>
        <ul>
          <li>Validation configurations</li>
          <li>Validator Explorer</li>
          <li>Validator Editor</li>
        </ul>
      </ul>


      <br><br>
      <button on:click={() => window.location.href = '/forms/manager'}>
        Try me
      </button>
    </div>
  </div>
  <br><br>


  <div class='card'>
    <div class='card-header'>Form Generator</div>
    <div class='card-body'>
      This element takes a configuration object and produces a reactive user
      interface.

      <br><br>
      Generating a form is as easy as this call:

      <br><br>
      <img src='static/images/FormGeneratorCode.png'
        alt='An image of the FormGenerator call.'/>

      <br><br>
      Where a configuration object looks like the this:

      <br><br>
      <img src='static/images/FormGeneratorConfig.png'
        alt='An image of the FormGenerator config.'/>
    </div>
  </div>
</div>



<style>
  img {
    border: 2px inset;
    max-width: calc(100% - 24px);
    /* max-width: 100%; */
    margin-left: auto;
  }
  .tile {
    border: 3px ridge;
    background-color: var(--pallete-0);
    padding: 24px;
  }

  .form-route {
    min-height: 93vh; /*  TODO general solution */
    max-width: 750px;
    margin: auto;
    margin-top: 12px;
  }
  p {
    margin: 24px;
    /* background-color: var(--pallete-0) */
  }
  .card-header {
    font-size: 24px;
    color: white;
    background-color: var(--pallete-2);

  }
  .card-body {
    margin: 12px;
  }

</style>


<!-- <FormManager/> -->
<!-- <DropDown bind:values={options} bind:value={option} null_option={true}/> -->
<!-- <ObjectEditor bind:object={config}/> -->
<!-- <FormEditor bind:config={config} bind:values={values}/> -->
<!-- <FormGenerator {config} /> -->


<script>
  // import FormManager from './form_manager.svelte';
  // import FormEditor from './form_editor.svelte';
  // import FormGenerator from './form_generator.svelte';
  // import ObjectEditor from '../utils/object_editor.svelte'
  // import DropDown from './inputs/drop_down.svelte'
  //
  // let config = {
  //   'type': 'form',
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
  // }
  // let values = {};

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
