export const useManifest = () => {
  return useAsyncData('manifest', () => $fetch('/api/manifest'))
}

