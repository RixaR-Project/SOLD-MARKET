# $Id: inc-html-trade.cgi 96 2004-03-12 12:25:28Z mu $

RequireFile('inc-html-ownerinfo.cgi');

my $itemlist="";
if($tp!=0 || !$MOBILE)
{
	$itemlist="<select name=itn>";
	my @sort;
	foreach(keys %itemlist){$sort[$_]=$ITEM[$_]->{sort}};
	foreach(0,grep($ITEM[$_]->{type}==$tp || !$tp,sort{$sort[$a] <=> $sort[$b]}keys(%itemlist)))
	{
		$itemlist.="<option value=\"$_\"".($_==$Q{itn}?' SELECTED':'').">".$ITEM[$_]->{name};
	}
	$itemlist.="</select>";
}

@itemlist=sort { $a->[7] <=> $b->[7] } @itemlist;

my($page,$pagestart,$pageend,$pagenext,$pageprev,$pagemax)
	=GetPage($Q{pg},$LIST_PAGE_ROWS,scalar(@itemlist));

$disp.="���f�Օi���X�g";
$disp.="<HR SIZE=\"1\">";

my $sitetaxrate=GetTradeTaxRate();
$disp.=$TB.$TR.$TD."���݂̗A�o�֐ŗ�".$TD.$sitetaxrate."%".$TD."�A�o�݌v".$TD."\\".($DTTradeOut+0).$TD."�A���݌v".$TD."\\".($DTTradeIn+0).$TRE.$TBE;
$disp.="<HR SIZE=\"1\">";

foreach my $cnt (0..$#ITEMTYPE)
{
	$disp.="<A HREF=\"$MYNAME?$USERPASSURL&tp=$cnt&t=2\">" if $cnt!=$tp;
	$disp.=GetTagImgItemType(0,$cnt) if $cnt && !$MOBILE;
	$disp.="&lt;" if $cnt==$tp;
	$disp.=$ITEMTYPE[$cnt];
	$disp.="&gt;" if $cnt==$tp;
	$disp.="</A>" if $cnt!=$tp;
	$disp.=" ";
}
$disp.="<hr size=\"1\">";

$disp.=<<"HTML" if $tp!=0 || !$MOBILE;
<form action="$MYNAME" $METHOD>
$USERPASSFORM
<input type=hidden name=tp value=\"$tp\">
<input type=hidden name=t value="2">
$itemlist
<input type=submit value="����">
</form>
HTML

$pagectrl=GetPageControl($pageprev,$pagenext,"t=2&itn=$Q{itn}&tp=$tp","",$pagemax,$page);
$disp.=$pagectrl."<HR SIZE=\"1\">";


$disp.=$TB;
$disp.=$TR.$TDNW."�I���܂�".$TDNW."���i".$TDNW."���i".$TDNW."�P��".$TDNW."����".$TDNW."��掞��".$TDNW."�A�o��".$TDNW."�R�����g".$TRE;
foreach my $cnt ($pagestart .. $pageend)
{
	my $item=$itemlist[$cnt];
	my $deny_trade=CheckItemFlag($item->[3],'notradein');
	
	my $lasttime=$TRADE_STOCK_TIME-$NOW_TIME+$item->[7];
	$disp.=$TR.$TDNW.($lasttime>0 ? GetTime2HMS($lasttime,1):'�܂��Ȃ�');
	$disp.="<br>".$item->[8]."<small>���葱</small>" if $item->[8];
	$disp.=$TD;
	$disp.="<A HREF=\"box-edit.cgi?$USERPASSURL&tradein=$item->[0]\">" if !$deny_trade && !$GUEST_USER;
	$disp.=GetTagImgItemType($item->[3]).$ITEM[$item->[3]]->{name};
	$disp.='[�A���s��]' if $deny_trade;
	$disp.="</A>" if !$deny_trade && !$GUEST_USER;
	
	$disp.=$TDNW."\\".$item->[5];
	$disp.=$TDNW."\@\\".int($item->[5]/$item->[4]).$TDNW.$item->[4].$ITEM[$item->[3]]->{scale};
	$disp.=$TDNW.GetTime2HMS(GetTimeDeal($item->[5],$item->[3],$item->[4]))."<br>";
	
	$disp.=$TDNW.$item->[1]."<br>".$item->[2].$TD.EscapeHTML($item->[6]);
	$disp.=$TRE;
	$disp.="<HR SIZE=\"1\">" if $MOBILE;
}
$disp.=$TBE;
#$disp.="<HR SIZE=1>";

#$disp.=$pagectrl;

1;
