
<!---- Body ---->

<div class="form-dashboard">

  <div class="form-selector">
    <h5>Explorer</h5>
    <br>

    <div class='radio-container'>
      <div>
        <input type='radio' id='existing' bind:group={radio_value} value='existing' />
        <label for='existing'>Select Existing</label>
      </div>

      <div>
        <input type='radio' id='new' bind:group={radio_value} value='new' />
        <label for='new'>Create New</label>
      </div>
    </div>
    <br>

    {#if radio_value == 'existing'}

      <DropDown
        bind:values={form_groups}
        bind:value={form_group}
        null_option={true}
        name='form_group'
        label="Form name:"
      />

      <DropDown
        bind:values={major_versions}
        bind:value={major_version}
        null_option={true}
        name='major_version'
        label="Major version:"
      />

      <DropDown
        bind:values={minor_versions}
        bind:value={minor_version}
        null_option={true}
        name='minor_version'
        label="Minor version:"
      />

      {#if minor_version != null}
        <br>
        <button disabled={!config_update} on:click={new_minor_version}>
          Save Minor Version
        </button>
        <button
          disabled={config_update || !minor_version}
          on:click={new_major_version}
        >
          Publish Major Version
        </button>

      {/if}

    {:else}

      <FormGenerator config={new_form_config} bind:values={new_form_values}/>

    {/if}

  </div>

  {#if config != null}
    <div class='form-editor'>

      <h5>Configuration</h5>
      <ObjectEditor bind:object={config}/>
      <br>

      {#if values != null}
        <h5>Value</h5>
        <ObjectEditor bind:object={values}/>
        <br>
      {/if}

      <h5>Raw HTML:</h5>
      <div class='raw-container'>
        <div class='code-block-disabled'>{raw_html}</div>
      </div>

    </div>
    <!-- <FormEditor bind:config={config} bind:values={values}/> -->

    {#if config != {}}
      <div class='form-preview'>
        <h5>Preview</h5>
        <br>
        <FormGenerator bind:raw={raw_html} bind:config={config} bind:values={values}/>
      </div>
    {/if}

  {/if}

</div>



<!---- Style ---->

<style>
  .form-dashboard {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    height: 92vh;
    /* flex-grow: 1; */
  }
  .radio-container {
    margin: 6px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  .form-selector {
    border: 2px outset;
    margin: 12px;
    /* margin-left: 0; */
    padding: 12px;
    width: 300px;
    max-height: 100%;
    /* width: 20%; */
  }
  .form-editor {
    border: 2px outset;
    margin: 12px;
    /* margin-left: 0; */
    padding: 12px;
    flex-grow: 1;
    /* max-width: 30%; */
    max-width: calc( (100% - 300px) * 0.6 );
    max-height: 100%;
    overflow-y: scroll;
  }
  .form-preview {
    border: 2px outset;
    margin: 12px;

    /* margin-left: 0; */
    padding: 12px;
    flex-grow: 1;
    max-height: 100%;
    /* min-height: 300px; */
    height: auto;
  }
  .raw-container {
    margin: 12px;
    /* max-width: 600px; */
    width: 100%;
  }
</style>



<script>

  import DropDown from './inputs/drop_down.svelte';
  // import FormEditor from './form_editor.svelte';
  import FormGenerator from './form_generator.svelte';
  import ObjectEditor from '../utils/object_editor.svelte'
  import {serialize, deserialize, deepcopy} from '../utils/serde.js'


  // // load config for given selection
  let form_cache_key;
  let form_group_configs;
  let form_groups;
  let form_group;
  let major_versions;
  let major_version;
  let minor_versions;
  let minor_version;
  let active_config;
  let config_update;
  let config;
  let values;
  let raw_html;


  $: console.log('form_group', form_group);
  $: console.log('major_versions', major_versions);
  $: console.log('major_version', major_version);
  $: console.log('minor_versions', minor_versions);
  $: console.log('minor_version', minor_version);
  $: console.log({form_group_configs});
  // $: console.log('fm config', config);
  // $: console.log('fm values', values);
  // $: console.log('fm values', values);
  // $: console.log('fm config', serialize(config));


  // wait until config loads and then load form_group_configs
  document.config.then((config) => {
    form_cache_key = config.project_name + '.form_group_configs';

    // try to load & parse the form group
    try {
      form_group_configs = deserialize(localStorage.getItem(form_cache_key));
      console.log({form_group_configs});
      // form_group = 'Contact Info'
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
            0: {},
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
            0: {},
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
  $: if (form_group_configs) {

    /// persist changes to form_group_configs to localStorage
    if (form_cache_key) {
      if (localStorage.getItem(form_cache_key) != serialize(form_group_configs) ) {
        localStorage.setItem(form_cache_key, serialize(form_group_configs));
        console.log(`saved form_group_configs to localStorage["${form_cache_key}"]`);
      }
    }

    // form_groups should be reactive to keys in form_group_configs
    form_groups = Object.keys(form_group_configs);
    // console.log('ser', serialize(form_group_configs['New Form'][0][1]));
    // console.log('de', deserialize(serialize(form_group_configs['New Form'][0][1])));
    // console.log({form_groups});
  }

  // statements reacive to (non-null) form_group values
  $: if (form_group == null) {
    // console.log('form_group reaction', form_group);
    // if (form_group == null) {
      major_versions = [];
      major_version = null;
    } else {
      major_versions = Object.keys(form_group_configs[form_group]);
      // major_version = major_versions[major_versions.length-1];
      // major_version = null;
    }
  // }

  // statements reacive to (non-null) major_version values
  $: if (major_version == null) {
    // console.log('major_version reaction', major_version);
    // if (major_version == null) {
      minor_versions = [];
      minor_version = null;
    } else {
      try {
        minor_versions = Object.keys(form_group_configs[form_group][major_version]);
      } catch (error) {
        major_version = null
      }
      // minor_version = minor_versions[minor_versions.length-1];
      // minor_version = null;
    }
  // }

  // $: if (minor_versions) {
  //   minor_version = null;
  // }

  $: if (minor_version) {
    // console.log('minor_version reaction', minor_version);
    // if (minor_version != null ) {
      version_selected(form_group, major_version, minor_version)
    } else {
      version_deselected()
    }
  // }

  function version_selected(form_group, major_version, minor_version) {
    version_deselected()
    console.log('version selected');
    active_config = form_group_configs[form_group][major_version][minor_version]
    try {
      config = deepcopy(active_config)
    } catch (error) {
    alert('ERROR in deepcopy: ' + serialize(active_config));
    }
  }


  function version_deselected() {
    console.log('version deselected');
    values = null;
    config = null;
    active_config = null;
  }


  function new_minor_version() {
    const new_minor_version = (parseInt(minor_version) + 1).toString();
    form_group_configs[form_group][major_version][new_minor_version] = config
    minor_version = new_minor_version
    alert(`Created new version: V${major_version}.${minor_version}`)
  }


  function new_major_version() {
    const new_major_version = (parseInt(major_version) + 1).toString();
    form_group_configs[form_group][new_major_version] = {"0": config}
    major_version = new_major_version
    minor_version = "0"
    alert(`Created new version: V${major_version}.${minor_version}`)
  }


  $: config_update = serialize(config) != serialize(active_config)

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
          form_group_configs[name] = {"0": {"0": {'type': 'form', 'items': []}}};
          new_form_values = null;
          radio_value = 'existing';
          form_group = name;
          major_version = null;
          minor_version = null;
        }
      }
    }]
  }

</script>
