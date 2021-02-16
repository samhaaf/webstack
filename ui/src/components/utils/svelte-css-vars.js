// export default (node, props) => {
//
//   Object.entries(props).forEach(([key, value]) => {
//     node.style.setProperty(`--${key}`, value);
//   });
//
//   return {
//     update(new_props) {
//       Object.entries(new_props).forEach(([key, value]) => {
//         node.style.setProperty(`--${key}`, value);
//         delete props[key];
//       });
//
//       Object.keys(props).forEach(name => {
//         // if (!original_style_elements.includes(name)) {
//           node.style.removeProperty(`--${name}`)
//         // }
//       });
//       props = new_props;
//     },
//   };
// };


export default (node, props) => {

  let original_style_elements = node.style.forEach((k,v) => k);

  Object.entries(props).forEach(([key, value]) => {
    node.style.setProperty(`--${key}`, value);
  });

  return {
    update(new_props) {
      Object.entries(new_props).forEach(([key, value]) => {
        node.style.setProperty(`--${key}`, value);
        delete props[key];
      });

      Object.keys(props).forEach(name =>
        node.style.removeProperty(`--${name}`),
      );
      props = new_props;
    },
  };
};
