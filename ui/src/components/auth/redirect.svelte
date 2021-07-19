

<script>
  export let href = '';
  export let return_to;
  // export let return_here;

  let redirect_url = href
  let question_mark = false;

  if (return_to != null) {
    if (!question_mark) {
      redirect_url += '?'
      question_mark = true
    }
    redirect_url += 'return_url=' + encodeURIComponent(return_to) + '&'
  }

  if (('return-here' in $$props) && ($$props['return_here'] != false)) {
    if (!question_mark) {
      redirect_url += '?'
      question_mark = true
    }
    console.log(2);
    let current_url = window.location.pathname+window.location.search
    redirect_url += 'return_url=' + encodeURIComponent(current_url) + '&'
  }

  // document.location.href = redirect_url
  window.location.replace(redirect_url);

</script>
