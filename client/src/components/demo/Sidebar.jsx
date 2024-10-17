export function Sidebar() {
  return (
    <>
      <div className="flex h-[100%] flex-col justify-between border-e bg-white ml-2">
        <div className="px-4 py-6 ">
          <span className="grid place-content-center rounded-lg text-teal-600  font-bold text-2xl shadow-[rgba(0,_0,_0,_0.24)_0px_3px_8px]">
            TweetLense
          </span>

          <ul className="mt-6 space-y-1">
            <li>
              <a
                href="#"
                className="block rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700"
              >
                About
              </a>
            </li>

            <li>
              <a
                href="#"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700"
              >
                Blog
              </a>
            </li>

            <li>
              <a
                href="#"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700"
              >
                Contact
              </a>
            </li>
          </ul>
        </div>

        <div className="sticky inset-x-0 bottom-0 border-t border-gray-100">
          <a
            href="#"
            className="flex items-center gap-2 bg-white p-4 hover:bg-gray-50"
          >
            <img
              alt=""
              src="https://images.unsplash.com/photo-1600486913747-55e5470d6f40?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80"
              className="size-10 rounded-full object-cover"
            />

            <div>
              <p className="text-xs">
                <strong className="block font-medium">Nishad Bhujbal</strong>

                <span> nishadbhujbal@gmail.com </span>
              </p>
            </div>
          </a>
        </div>
      </div>
    </>
  );
}

// c3ccaecb001a45e0864b03adcc94ca9c
