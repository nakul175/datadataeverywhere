import 'server-only';

function checkedUrl(value: string | undefined, fallback: string) {
  const url = new URL(value || fallback);
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash)
    throw new Error('Public tool URLs must use HTTPS without credentials or query parameters.');
  return url.toString();
}

export function publicUrls() {
  return {
    nocodb: checkedUrl(
      process.env.NOCODB_PUBLIC_URL,
      'https://nocodb.datadataeverywhere.aplyd.org',
    ),
    tasks: checkedUrl(process.env.TASKS_PUBLIC_URL, 'https://sheethappensofficer.aplyd.org'),
  };
}
