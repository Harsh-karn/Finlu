import { Bell, User } from 'lucide-react'

export function Header() {
  return (
    <header className="h-16 border-b border-[#2a2a4e] bg-[#1a1a2e]/80 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-10 text-white">
      <div className="flex items-center">
        {/* Breadcrumbs or Page Title could go here */}
      </div>
      
      <div className="flex items-center space-x-4">
        <button className="p-2 rounded-full hover:bg-[#2a2a4e] transition-colors relative">
          <Bell size={20} />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <div className="flex items-center space-x-2 p-2 rounded-full hover:bg-[#2a2a4e] transition-colors cursor-pointer">
          <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center">
            <User size={16} />
          </div>
          <span className="text-sm font-medium">User</span>
        </div>
      </div>
    </header>
  )
}
