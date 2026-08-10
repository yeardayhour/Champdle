export const apiLanguages = () =>
  $fetch<Array<string>>(`${apiBase()}/languages`)

export const apiChampions = () => $fetch<Array<Champion>>(`${apiBase()}/champions`)

export const apiChampionNameMap = (language: string) =>
  $fetch<Array<LocalName>>(`${apiBase()}/champion_name_map/${language}`)

export const apiRank = (puzzle_number: number) =>
  $fetch<Array<GuessResult>>(`${apiBase()}/rank/${puzzle_number}`)

export const apiGuess = (puzzle_number: number, name: string) =>
  $fetch<GuessResult>(`${apiBase()}/guess/${puzzle_number}?name=${encodeURIComponent(name)}`)

export const apiSaveRecord = (payload: {
  nickname?: string
  puzzle_number: number
  guess_count: number
  best_rank: number
  worst_rank: number
}) =>
  $fetch<{ status: string; message: string; record: any }>(`${apiBase()}/record`, {
    method: "POST",
    body: payload,
  })

export const apiGetRecords = (puzzle_number: number) =>
  $fetch<Array<any>>(`${apiBase()}/records/${puzzle_number}`)

