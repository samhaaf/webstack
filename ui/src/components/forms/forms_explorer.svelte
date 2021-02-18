
<!---- Script ---->

<script>
  import FormEditor from './form_editor.svelte';
  import FormGenerator from './form_generator.svelte';
  import {serialize, deserialize} from '../utils/serde.js'


  // // load config for given selection
  let form_cache_key;
  let form_group_configs;
  let form_groups;
  let form_group;
  let major_versions;
  let major_version;
  let minor_versions;
  let minor_version;
  let config;
  let values = {};


  $: console.log('major_versions', major_versions);
  $: console.log('major_version', major_version);
  $: console.log('minor_versions', minor_versions);
  $: console.log('minor_version', minor_version);
  $: console.log('ex config', config);
  $: console.log('ex values', values);

  function new_form(name) {
    form_group_configs = [
      ...form_group_configs,
      {'name': values.items.form_name.value}
    ];
    new_form_values = null;
    radio_value = 'existing';
  }

  // wait until config loads and then load form_group_configs
  document.config.then((config) => {
    form_cache_key = config.project_name + '.form_group_configs';

    // try to load & parse the form group
    try {
      form_group_configs = deserialize(localStorage.getItem(form_cache_key));
      console.log('form_group_configs', form_group_configs);
    } catch (error) {
      console.log('failed to deserialize form_group_configs from localStorage:', error);
    }

    // save updates to form_group_configs
    if (form_group_configs != null) {
      console.log(`loaded form_group_configs from localStorage["${form_cache_key}"]`);
    } else {
      console.log('using default form_group_configs');
      form_group_configs = {
        'Contact Info': {
          0: {
            1: {
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
          }
        },
        'New Form': {
          0: {
            1: {
              type: 'form',
              items: [{
                type: 'string',
                label: 'Form name:',
                name: 'form_name'
              },{
                type: 'submit',
                text: 'Create',
                action: (values) => { new_form(values.items.form_name.value) }
              }]
            }
          }
        }
      }
    }
  })


  // statements reactive to (non-null) form_group_configs values
  $: if (form_group_configs ) {

    /// persist changes to form_group_configs to localStorage
    if (form_cache_key) {
      if (localStorage.getItem(form_cache_key) != serialize(form_group_configs) ) {
        localStorage.setItem(form_cache_key, serialize(form_group_configs));
        console.log(`saved form_group_configs to localStorage["${form_cache_key}"]`);
      }
    }

    // form_groups should be reactive to keys in form_group_configs
    form_groups = Object.keys(form_group_configs);
    console.log('ser', serialize(form_group_configs['New Form'][0][1]));
    console.log('de', deserialize(serialize(form_group_configs['New Form'][0][1])));
  }


  // statements reacive to (non-null) form_group values
  $: if (form_group) {
    major_versions = Object.keys(form_group_configs[form_group]);
    major_version = major_versions[major_versions.length-1];
  } else {
    major_versions = null;
    major_version = null;
  }


  // statements reacive to (non-null) major_version values
  $: if (major_version) {
    minor_versions = Object.keys(form_group_configs[form_group][major_version]);
    minor_version = minor_versions[minor_versions.length-1];
    console.log('updating config');
    values = {};
    config = form_group_configs[form_group][major_version][minor_version]
  } else {
    minor_versions = null;
    minor_version = null;
    values = {};
    config = null;
  }


  // radio to switch select panels
  // TODO type: radio-panels
  let radio_value = 'existing';


  // Config object for creating a new form
  let new_form_values;
  let new_form_config = {
    type: 'form',
    items: [{
      type: 'string',
      label: 'Form name:',
      name: 'form_name'
    },{
      type: 'submit',
      text: 'Create',
      action() {
        const name = new_form_values.items.form_name.value;
        if ( form_group_configs.hasOwnProperty(name)) {
          alert(`Form name "${name}" already exists. Please choose another.`)
        } else {
          form_group_configs[name] = {0: {0: {}}};
          new_form_values = null;
          radio_value = 'existing';
        }
      }
    }]
  }

</script>

<!---- Body ---->

<div class="form-selector">
  <h3>Form Selector</h3>
  <br>

  <input type='radio' id='existing' bind:group={radio_value} value='existing' />
  <label for='existing'>Select Existing</label>

  <input type='radio' id='new' bind:group={radio_value} value='new' />
  <label for='new'>Create New</label>

  {#if radio_value == 'existing'}

    <div class="form-groups-container">
      <label for='group-selector'>Form name:</label>
      <select bind:value={form_group} name='group-selector'>
        {#if form_groups != null}
          <option value={null}>---</option>
          {#each form_groups as group}
            <option value={group}>{group}</option>
          {/each}
        {/if}
      </select>
    </div>

    <div class="major-version-container">
      <label for='major-version-selector'>Major version:</label>
      <select bind:value={major_version} name='major-version-selector'>
        {#if major_versions != null}
          {#each major_version as version}
            <option value={version}>{version}</option>
          {/each}
        {/if}
      </select>
    </div>

    <div class="minor-version-container">
      <label for='minor-version-selector'>Minor version:</label>
      <select bind:value={minor_version} name='minor-version-selector'>
        {#if minor_versions != null}
          {#each minor_version as version}
            <option value={version}>{version}</option>
          {/each}
        {/if}
      </select>
    </div>

  {:else}

    <FormGenerator config={new_form_config} bind:values={new_form_values}/>

  {/if}

</div>

{#if config != null}
  <FormEditor bind:config={config} bind:values={values}/>
{/if}

<!---- Style ---->

<style>
  .form-selector {
    border: 2px outset;
    margin: 12px;
    padding: 6px;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }
  select {
    min-width: 200px;
  }
</style>
