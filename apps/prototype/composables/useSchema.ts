export const useSchema = (journeyKey: string) => {
  return useAsyncData(`schema:${journeyKey}`, () => $fetch(`/api/schema/${journeyKey}`))
}
