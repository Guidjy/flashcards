// hooks
import { useBreakpoint } from "../hooks/useBreakpoint"
// components
import Dock from "../components/Dock";
import Navbar from "../components/Navbar";


export default function MainLayout({ children }) {
  
  const breakpoint = useBreakpoint();

  return (
    <>
      {breakpoint === 'xs' || breakpoint === 'sm' ? (
        <Dock />
      ) : (
        <Navbar />
      )}
      <div className="flex justify-center w-full min-h-screen bg-base-200">
        <div className="flex flex-col justify-items-center w-full md:w-4/5 lg:w-2/3 xl:w-1/2 p-5 md:p-10">
          {children}
        </div>
      </div>
    </>
  )
}