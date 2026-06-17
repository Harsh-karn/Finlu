import NextAuth from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import api from "@/lib/api"

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
          const res = await api.post("/auth/login", {
            username: credentials?.username,
            password: credentials?.password
          }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
          })
          
          if (res.data && res.data.access_token) {
            return { id: "1", accessToken: res.data.access_token } as any
          }
          return null
        } catch (e) {
            return null
        }
      }
    })
  ],
  pages: {
    signIn: '/login',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = (user as any).accessToken
      }
      return token
    },
    async session({ session, token }) {
      (session as any).accessToken = token.accessToken
      return session
    }
  }
})

export { handler as GET, handler as POST }
