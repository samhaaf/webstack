
<script>
  /*
    TODO:
      * take style property and add it to the div
      * take border property
      * make it not a Card with a title and header
  */

  import {Card, CardBody, CardTitle, CardHeader} from 'sveltestrap';

  export let title = undefined;
  export let header = undefined;

  let card_classes = [];
  let header_classes = [];
  let title_classes = [];
  let body_classes = [];

  // set default margin and padding
  if ('m-0' in $$props){ card_classes = [...card_classes, 'm-0'] }
  if ('m-1' in $$props){ card_classes = [...card_classes, 'm-1'] }
  if ('m-2' in $$props){ card_classes = [...card_classes, 'm-2'] }
  if ('m-3' in $$props){ card_classes = [...card_classes, 'm-3'] }
  if ('m-4' in $$props){ card_classes = [...card_classes, 'm-4'] }
  if ('p-0' in $$props){ body_classes = [...body_classes, 'p-0'] }
  if ('p-1' in $$props){ body_classes = [...body_classes, 'p-1'] }
  if ('p-2' in $$props){ body_classes = [...body_classes, 'p-2'] }
  if ('p-3' in $$props){ body_classes = [...body_classes, 'p-3'] }
  if ('p-4' in $$props){ body_classes = [...body_classes, 'p-4'] }

  // set card margin and padding
  if ('cm-0' in $$props){ card_classes = [...card_classes, 'm-0'] }
  if ('cm-1' in $$props){ card_classes = [...card_classes, 'm-1'] }
  if ('cm-2' in $$props){ card_classes = [...card_classes, 'm-2'] }
  if ('cm-3' in $$props){ card_classes = [...card_classes, 'm-3'] }
  if ('cm-4' in $$props){ card_classes = [...card_classes, 'm-4'] }
  if ('cp-0' in $$props){ card_classes = [...card_classes, 'p-0'] }
  if ('cp-1' in $$props){ card_classes = [...card_classes, 'p-1'] }
  if ('cp-2' in $$props){ card_classes = [...card_classes, 'p-2'] }
  if ('cp-3' in $$props){ card_classes = [...card_classes, 'p-3'] }
  if ('cp-4' in $$props){ card_classes = [...card_classes, 'p-4'] }

  // set header margin and padding
  if ('hm-0' in $$props){ header_classes = [...header_classes, 'm-0'] }
  if ('hm-1' in $$props){ header_classes = [...header_classes, 'm-1'] }
  if ('hm-2' in $$props){ header_classes = [...header_classes, 'm-2'] }
  if ('hm-3' in $$props){ header_classes = [...header_classes, 'm-3'] }
  if ('hm-4' in $$props){ header_classes = [...header_classes, 'm-4'] }
  if ('hp-0' in $$props){ header_classes = [...header_classes, 'p-0'] }
  if ('hp-1' in $$props){ header_classes = [...header_classes, 'p-1'] }
  if ('hp-2' in $$props){ header_classes = [...header_classes, 'p-2'] }
  if ('hp-3' in $$props){ header_classes = [...header_classes, 'p-3'] }
  if ('hp-4' in $$props){ header_classes = [...header_classes, 'p-4'] }

  // set title margin and padding
  if ('tm-0' in $$props){ title_classes = [...title_classes, 'm-0'] }
  if ('tm-1' in $$props){ title_classes = [...title_classes, 'm-1'] }
  if ('tm-2' in $$props){ title_classes = [...title_classes, 'm-2'] }
  if ('tm-3' in $$props){ title_classes = [...title_classes, 'm-3'] }
  if ('tm-4' in $$props){ title_classes = [...title_classes, 'm-4'] }
  if ('tp-0' in $$props){ title_classes = [...title_classes, 'p-0'] }
  if ('tp-1' in $$props){ title_classes = [...title_classes, 'p-1'] }
  if ('tp-2' in $$props){ title_classes = [...title_classes, 'p-2'] }
  if ('tp-3' in $$props){ title_classes = [...title_classes, 'p-3'] }
  if ('tp-4' in $$props){ title_classes = [...title_classes, 'p-4'] }

  // set body margin and padding
  if ('bm-0' in $$props){ body_classes = [...body_classes, 'm-0'] }
  if ('bm-1' in $$props){ body_classes = [...body_classes, 'm-1'] }
  if ('bm-2' in $$props){ body_classes = [...body_classes, 'm-2'] }
  if ('bm-3' in $$props){ body_classes = [...body_classes, 'm-3'] }
  if ('bm-4' in $$props){ body_classes = [...body_classes, 'm-4'] }
  if ('bp-0' in $$props){ body_classes = [...body_classes, 'p-0'] }
  if ('bp-1' in $$props){ body_classes = [...body_classes, 'p-1'] }
  if ('bp-2' in $$props){ body_classes = [...body_classes, 'p-2'] }
  if ('bp-3' in $$props){ body_classes = [...body_classes, 'p-3'] }
  if ('bp-4' in $$props){ body_classes = [...body_classes, 'p-4'] }

  // card align
  if ('left' in $$props | 'l' in $$props ){ card_classes += ' text-left' }
  if ('center' in $$props | 'c' in $$props ){ card_classes += ' text-center' }
  if ('right' in $$props | 'r' in $$props ){ card_classes += ' text-right' }

  // header align
  if ('header-left' in $$props | 'hl' in $$props){ header_classes = [...header_classes, 'text-left']; }
  if ('header-center' in $$props | 'hc' in $$props){ header_classes = [...header_classes, 'text-center']; }
  if ('header-right' in $$props | 'hr' in $$props){ header_classes = [...header_classes, 'text-right']; }

  // body align
  if ('title-left' in $$props | 'tl' in $$props){ title_classes = [...title_classes, 'text-left']; }
  if ('title-center' in $$props | 'tc' in $$props){ title_classes = [...title_classes, 'text-center']; }
  if ('title-right' in $$props | 'tr' in $$props){ title_classes = [...title_classes, 'text-right']; }

  // body align
  if ('body-left' in $$props | 'bl' in $$props){ body_classes = [...body_classes, 'text-left']; }
  if ('body-center' in $$props | 'bc' in $$props){ body_classes = [...body_classes, 'text-center']; }
  if ('body-right' in $$props | 'br' in $$props){ body_classes = [...body_classes, 'text-right']; }

  // if ('row' in $$props) { body_classes += [...card_classes, 'row'] }

</script>

<Card class={card_classes}>

  {#if header!=null}
    <CardHeader class={ header_classes }>{ header }</CardHeader>
  {/if}

  {#if title!=null}
    <CardTitle class={ title_classes }>{ title }</CardTitle>
  {/if}

  <CardBody class={ body_classes }><slot/></CardBody>
</Card>
