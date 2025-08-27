import { useState, useEffect } from "react";


// tailwind breakpoints
const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  "2xl": 1536,
};

export function useBreakpoint() {
  const [breakpoint, setBreakpoint] = useState(getBreakpoint(window.innerWidth));

  useEffect(() => {
    // gets the new width and updates breakpoint.
    function handleResize() {
      setBreakpoint(getBreakpoint(window.innerWidth));
    }

    // adds a resize event listener to window when the component is mounted
    window.addEventListener("resize", handleResize);
    // also cleans up the event listener when the component unmounts (best practice apparently)
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return breakpoint;
}

function getBreakpoint(width) {
  if (width < breakpoints.sm) return "xs";
  if (width < breakpoints.md) return "sm";
  if (width < breakpoints.lg) return "md";
  if (width < breakpoints.xl) return "lg";
  if (width < breakpoints["2xl"]) return "xl";
  return "2xl";
}


/*
why useBreakpoint works: since an event listener is added to window when the component is mounted,
whe don't need to do somehting like adding the window object to the useEffect array, because everytime
the window size changes, handleResize is ran 
*/