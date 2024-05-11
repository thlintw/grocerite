
<div class="
        flex flex-col
        w-full h-full gap-5
        pb-32 lg:pb-3
        mt-2
    ">
        <div class="w-full bg-orange-50 px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl shadow-grocerite-neutral-100-sm">
            <div class="flex items-center w-full gap-2 border-b-2 border-b-neutral-200/70 animate-pulse pb-2">
                <div class="text-xl lg:text-2xl h-7 w-28 animate-pulse bg-neutral-200 rounded-lg"></div>
                <div class="ml-auto w-8 lg:w-10 bg-neutral-200 rounded-full animate-pulse h-8 lg:h-10" />
            </div>
            <div class="flex flex-col gap-2 mb-2">
                {#each {length: 3} as _, i}
                    <div class="flex items-center text-neutral-700">
                        <div class="relative bg-neutral-200 w-9 h-9 rounded-lg shrink-0
                            flex justify-center items-center animate-pulse">
                        </div>
                        <div class="text-xl font-mono text-center w-16 font-bold shrink-0 h-3"></div>
                        <div class="text-base lg:text-lg overflow-hidden text-ellipsis text-nowrap pr-2 flex items-center
                            bg-neutral-200 animate-pulse h-5 w-40 rounded-lg">
                            
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>