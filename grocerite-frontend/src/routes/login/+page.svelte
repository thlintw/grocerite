<svelte:head>
	<title>{$_('login_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="household" />
</svelte:head>

<script lang="ts">
	import { _, locale, locales } from 'svelte-i18n';
	import login1 from '$lib/images/login1.png';
	import swoosh from '$lib/images/swoosh.svg';
	import logoFull from '$lib/images/logo-full.png';
	import google from '$lib/images/google.png';
    import { get } from 'svelte/store';
	
	$: l = $locale;

	$: fontFamilyCls = l == 'ja-JP' || l == 'zh-TW' ? 'font-sans' : 'font-berkshire';


</script>

<div class="bg-orange-50 w-full min-h-full max-h-full flex overflow-hidden">
	<div class="w-7/12 h-full flex relative bg-orange-50">
		<div class="h-full w-[28rem] absolute bottom-0 right-0 z-10">
			<img src={swoosh} alt="swoosh" class="h-full w-full"/>
		</div>
		<div class="h-full w-full z-20 flex items-center overflow-clip">
			<img src={login1} alt="login" class="w-[36rem] ml-auto mt-24 mr-20"/>	
		</div>
	</div>
	<div class="flex justify-start bg-orange-100 h-full w-5/12">
		<div class="flex flex-col justify-center items-center">
			<div class="flex flex-col items-center">
				<div class="relative">
					<img src={logoFull} alt="logo" class="w-[22rem]"/>
					<span class="text-2xl font-bold text-center mt-8
						absolute right-5 -bottom-4
						{fontFamilyCls} text-orange-500">
						{$_('login_catchPhrase')}
					</span>
				</div>
			</div>
			<div class="flex flex-col gap-5 mt-32">
				<div class="bg-white w-72 py-3 rounded-lg flex items-center justify-center shadow-md">
					<img src={google} alt="google" class="w-6 h-6"/>
					<span class="text-neutral-500 font-bold ml-4 text-base">{$_('login_continueWithGoogle')}</span>
				</div>
				<div class="bg-orange-50/50 lg:bg-transparent border-2 border-orange-500 w-72 py-3 rounded-lg flex items-center justify-center">
					<span class="text-orange-500 font-bold text-base">{$_('login_lookingAround')}</span>
				</div>
			</div>
		</div>
	</div>

</div>