export default function routeMatchesName(route, name) {
  for (let element of route.matched) {
    if (element.name === name) {
      return true;
    }
  }
  return false;
}
