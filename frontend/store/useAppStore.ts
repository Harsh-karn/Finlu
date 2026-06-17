import { create } from 'zustand'

interface AppState {
  user: any | null
  setUser: (user: any) => void
  logout: () => void
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null })
}))
